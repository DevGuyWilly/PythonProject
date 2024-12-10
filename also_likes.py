from collections import Counter


class AlsoLikesAnalyzer:
    def __init__(self, data):
        self.data = data

    def get_document_readers(self, doc_id):
        """Get all unique visitors who read a specific document"""
        readers = {entry.get('visitor_uuid') for entry in self.data
                   if entry.get('subject_doc_id') == doc_id and
                   entry.get('event_type') in ['reader', 'pageread', 'pagereadtime']}
        return readers

    def get_also_likes(self, doc_id, visitor_id=None, sort_function=None):
        """Get related documents based on common readers"""
        # Get readers of the input document
        doc_readers = self.get_document_readers(doc_id)
        if not doc_readers:
            return []

        # Count documents read by these readers (excluding the input document)
        related_docs = Counter()
        for entry in self.data:
            if (entry.get('visitor_uuid') in doc_readers and
                    entry.get('subject_doc_id') != doc_id and
                    entry.get('event_type') in ['reader', 'pageread', 'pagereadtime']):
                related_docs[entry.get('subject_doc_id')] += 1

        # Sort results if a sort function is provided
        if sort_function:
            return sort_function(related_docs)
        return related_docs.most_common()

    def generate_graph(self, doc_id, visitor_id, results):
        """Generate a dot graph showing the relationships between documents and readers"""
        from graphviz import Digraph

        dot = Digraph(comment='Also Likes Graph')
        dot.attr(ranksep='1.5', ratio='compress', size='15,22', rankdir='TB')

        # Create header nodes
        dot.node('Readers', 'Readers', shape='plaintext', fontsize='16')
        dot.node('Documents', 'Documents', shape='plaintext', fontsize='16')
        dot.edge('Readers', 'Documents', 'Size: 1m')

        # Helper function to get last 4 chars of UUID
        def short_id(id_str):
            return id_str[-4:] if id_str else id_str

        # Get all readers who read the input document
        original_readers = self.get_document_readers(doc_id)

        # Get all readers who read any of the related documents
        all_readers = set()
        all_readers.update(original_readers)
        for related_doc, _ in results:
            related_readers = self.get_document_readers(related_doc)
            all_readers.update(related_readers)

        # Create readers subgraph at top
        with dot.subgraph(name='cluster_readers') as s:
            s.attr(rank='same')
            # Add reader nodes
            for reader in all_readers:
                reader_id = short_id(reader)
                # Shade the input visitor if provided
                if visitor_id and reader == visitor_id:
                    s.node(reader_id, reader_id, shape='box', style='filled', color='.3 .9 .7')
                else:
                    s.node(reader_id, reader_id, shape='box')

        # Create documents subgraph at bottom
        with dot.subgraph(name='cluster_documents') as s:
            s.attr(rank='same')
            # Add input document (shaded)
            s.node(short_id(doc_id), short_id(doc_id), shape='circle', style='filled', color='.3 .9 .7')
            # Add related documents
            for related_doc, _ in results:
                s.node(short_id(related_doc), short_id(related_doc), shape='circle')

        # Add edges (arrows) from readers to documents
        for reader in all_readers:
            reader_id = short_id(reader)
            # Add edge to input document if they read it
            if reader in original_readers:
                dot.edge(reader_id, short_id(doc_id))
            # Add edges to related documents if they read them
            for related_doc, _ in results:
                if reader in self.get_document_readers(related_doc):
                    dot.edge(reader_id, short_id(related_doc))

        # Render the graph to a PNG file
        # output_file = f'also_likes_graph_{short_id(doc_id)}.png'
        output_file = f'also_likes_graph'
        dot.render(output_file, format='png', cleanup=True)

        return dot


def display_also_likes(results, limit=10):
    """Display the top 'Also Likes' results"""
    if not results:
        print("\nNo related documents found.")
        return

    print("\nTop 'Also Likes' Documents:")
    print("-" * 70)
    print(f"{'Rank':<6}{'Document ID':<50}{'Reader Count':<10}")
    print("-" * 70)

    for i, (doc_id, count) in enumerate(results[:limit], 1):
        print(f"{i:<6}{doc_id:<50}{count:<10}")
