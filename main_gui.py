# gui.py
from PIL import Image, ImageTk  # Add this import at the top of your file
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from main import analyze_document_views, analyze_browsers, analyze_reader_profiles, AlsoLikesAnalyzer, \
    display_also_likes, load_json_data, display_top_readers
from also_likes import AlsoLikesAnalyzer
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Create a style for ttk widgets
style = ttk.Style()
style.configure("TEntry", fieldbackground='lightgrey', foreground='black')  # Set colors

data = None


# Load your data (you might want to adjust the path)


class MainGUI:
    def __init__(self, root):
        """
        Initialize the main GUI window and its widgets.
        """

        # Set up main window
        root.title("F21SC_Group13")
        root.geometry("1038x698")
        root.configure(bg="white")

        self.data = None
        self.root = root
        self.alsolikes = None  # AlsoLikesAnalyzer(self.data)

        # View Frame
        # View Frame for displaying results
        self.view_frame = tk.LabelFrame(
            root,
            text="View Results",
            bg="black",
            fg="white",
            font=("Helvetica", 12, "bold"),
        )
        self.view_frame.place(relx=0.039, rely=0.0, relheight=0.38, relwidth=0.934)

        self.view_text = tk.Text(
            self.view_frame,
            bg="white",
            fg="black",
            font=("Helvetica", 10),
            wrap=tk.WORD,

        )
        self.view_text.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for the Text widget
        self.scrollbar = tk.Scrollbar(self.view_text, command=self.view_text.yview)
        self.view_text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load JSON File Button
        self.load_button = tk.Button(
            root,
            text="Load JSON File",
            bg="black",
            fg="white",
            font=("Helvetica", 12),
            command=self.load_json_file
        )
        self.load_button.place(relx=0.039, rely=0.387, height=40, width=974)

        # Analyze Document Views Frame
        self.doc_frame = tk.LabelFrame(
            root,
            text="Analyze Document Views",
            bg="white",
            fg="black",
            font=("Helvetica", 12, "bold"),

        )
        self.doc_frame.place(relx=0.039, rely=0.444, relheight=0.119, relwidth=0.935)

        self.doc_label = tk.Label(
            self.doc_frame,
            text="Enter Document ID:",
            bg="white",
            fg="black",
            font=("Helvetica", 10),
        )
        self.doc_label.place(relx=0.01, rely=0.4)

        self.doc_entry = tk.Entry(
            self.doc_frame,
            font=("Helvetica", 10),
            bg="lightgray",
            fg="black",
        )
        self.doc_entry.place(relx=0.15, rely=0.4, relwidth=0.6)

        self.generate_button = tk.Button(
            self.doc_frame,
            text="Generate",
            bg="black",
            fg="white",
            font=("Helvetica", 10),
            command=self.analyze_document_views_gui
        )
        self.generate_button.place(relx=0.8, rely=0.35)

        # Top Readers Frame
        self.readers_frame = tk.LabelFrame(
            root,
            text="Analyze Top Readers",
            bg="white",
            fg="black",
            font=("Helvetica", 12, "bold"),
        )
        self.readers_frame.place(relx=0.039, rely=0.573, relheight=0.106, relwidth=0.935)

        self.readers_button = tk.Button(
            self.readers_frame,
            text="Top Readers",
            bg="black",
            fg="white",
            font=("Helvetica", 10),
            command=self.analyze_top_readers
        )
        self.readers_button.place(relx=0.15, rely=0.3, relwidth=0.7)

        # Also Likes Frame
        self.also_likes_frame = tk.LabelFrame(
            root,
            text="Also Likes",
            bg="white",
            fg="black",
            font=("Helvetica", 12, "bold"),
        )
        self.also_likes_frame.place(relx=0.039, rely=0.688, relheight=0.288, relwidth=0.461)

        self.al_doc_label = tk.Label(
            self.also_likes_frame,
            text="Enter Document ID:",
            bg="white",
            fg="black",
            font=("Helvetica", 10),
        )
        self.al_doc_label.place(relx=0.05, rely=0.15)

        self.al_doc_entry = tk.Entry(
            self.also_likes_frame,
            bg="lightgray",
            fg="black",
            font=("Helvetica", 10),
        )
        self.al_doc_entry.place(relx=0.05, rely=0.25, relwidth=0.9)

        self.al_visitor_label = tk.Label(
            self.also_likes_frame,
            text="Enter Visitor ID (Optional):",
            bg="white",
            fg="black",
            font=("Helvetica", 10),
        )
        self.al_visitor_label.place(relx=0.05, rely=0.45)

        self.al_visitor_entry = tk.Entry(
            self.also_likes_frame,
            bg="lightgray",
            fg="black",
            font=("Helvetica", 10),
        )
        self.al_visitor_entry.place(relx=0.05, rely=0.55, relwidth=0.9)

        self.recommendation_button = tk.Button(
            self.also_likes_frame,
            text="Recommendations",
            bg="black",
            fg="white",
            font=("Helvetica", 10),
            command=self.analyze_also_likes
        )
        self.recommendation_button.place(relx=0.05, rely=0.8, width=200)

        self.graph_button = tk.Button(
            self.also_likes_frame,
            text="Graph",
            bg="black",
            fg="white",
            font=("Helvetica", 10),
            command=self.generate_also_likes_graph
        )
        self.graph_button.place(relx=0.55, rely=0.8, width=200)

        # Analyze Browser Frame
        self.browser_frame = tk.LabelFrame(
            root,
            text="Analyze Browser",
            bg="white",
            fg="black",
            font=("Helvetica", 12, "bold"),
        )
        self.browser_frame.place(relx=0.511, rely=0.688, relheight=0.288, relwidth=0.462)

        self.main_browser_button = tk.Button(
            self.browser_frame,
            text="Main Browser Names",
            bg="black",
            fg="white",
            font=("Helvetica", 10),
            command=self.analyze_browser_usage_main
        )
        self.main_browser_button.place(relx=0.1, rely=0.2, width=400)

        self.full_browser_button = tk.Button(
            self.browser_frame,
            text="Full Identifiers",
            bg="black",
            fg="white",
            font=("Helvetica", 10),
            command=self.analyze_browser_usage_full
        )
        self.full_browser_button.place(relx=0.1, rely=0.55, width=400)

    def plot_histogram(self, data, title, xlabel, ylabel="Number of Views"):
        """Embed the histogram in a Tkinter window."""
        if not data:
            messagebox.showerror("Error", "No data available for plotting.")
            return

        # Create a new window for the plot
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("800x600")

        # Create Matplotlib Figure
        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(111)
        ax.bar(data.keys(), data.values())
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', rotation=45)

        # Embed the figure in the Tkinter Toplevel
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        # Add a Close Button
        close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=10)

    # Choice 1
    def analyze_document_views_gui(self):
        document_id = self.doc_entry.get()
        if document_id:
            country_counts, continent_counts = analyze_document_views(self.data, document_id)
            if country_counts:
                self.plot_histogram(country_counts, f"Views by Country for Document {document_id}", "Country Code")
                self.plot_histogram(continent_counts, f"Views by Continent for Document {document_id}", "Continent")
            else:
                messagebox.showinfo("Result", f"No views found for document {document_id}")

    # Choice 2
    def analyze_browser_usage_full(self):
        full_browsers, _ = analyze_browsers(self.data)
        self.plot_histogram(full_browsers, "Views by Full Browser Identifier", "Browser User Agent")

    # Choice 3
    def analyze_browser_usage_main(self):
        _, main_browsers = analyze_browsers(self.data)
        self.plot_histogram(main_browsers, "Views by Main Browser Type", "Browser Name")

    # Choice 4
    def analyze_top_readers(self):
        """Analyze and display top readers."""
        if not self.data:
            messagebox.showerror("Error", "Please load a JSON file first.")
            return

        top_readers = analyze_reader_profiles(self.data)
        results = "\n".join(
            [f"{i + 1}. {reader['uuid']} - {reader['total_time_mins']} mins"
             for i, reader in enumerate(top_readers)]
        )
        self.display_text(f"Top Readers:\n{results}")

    def display_text(self, content):
        """Display text in the view frame."""
        self.view_text.delete("1.0", tk.END)  # Clear the current text
        self.view_text.insert(tk.END, content)

    # Choice 5
    def analyze_also_likes(self):
        # analyzer = AlsoLikesAnalyzer(data)
        doc_id = self.al_doc_entry.get()
        visitor_id = self.al_visitor_entry.get() or None

        if not doc_id:
            messagebox.showwarning("Input Error", "Document ID is required for analysis.")
            return

        results = self.alsolikes.get_also_likes(doc_id, visitor_id)
        self.display_text(f"Also Likes Recommendations:\n{results}")

    # Choice 6
    # def generate_also_likes_graph(self):
    #     #analyzer = AlsoLikesAnalyzer(data)
    #     doc_id = self.al_doc_entry.get()
    #     visitor_id = self.al_visitor_entry.get() or None

    #     if not doc_id:
    #         messagebox.showwarning("Input Error", "Document ID is required for graph generation.")
    #         return

    #     results = self.alsolikes.get_also_likes(doc_id, visitor_id)
    #     if results:
    #         graph = self.alsolikes.generate_graph(doc_id, visitor_id, results[:10])

    #         messagebox.showinfo("Success", "Graph has been generated as 'also_likes_graph.png'")
    #     else:
    #         messagebox.showinfo("Result", "No data available to generate graph.")
    def generate_also_likes_graph(self):
        doc_id = self.al_doc_entry.get()
        visitor_id = self.al_visitor_entry.get() or None

        if not doc_id:
            messagebox.showwarning("Input Error", "Document ID is required for graph generation.")
            return

        results = self.alsolikes.get_also_likes(doc_id, visitor_id)
        if results:
            # Generate the graph
            graph = self.alsolikes.generate_graph(doc_id, visitor_id, results[:10])

            # File path for the generated image
            output_file = "also_likes_graph.png"

            if os.path.exists(output_file):
                # Open the generated image in a new Tkinter window
                self.display_image(output_file)
                messagebox.showinfo("Success", f"Graph has been generated as '{output_file}'")
            else:
                messagebox.showerror("Error", "Graph generation failed or file not found.")
        else:
            messagebox.showinfo("Result", "No data available to generate graph.")

    def display_image(self, image_path):
        """Display an image in a new Tkinter window."""
        try:
            # Ensure root window exists
            if not self.root or not self.root.winfo_exists():
                self.root = tk.Tk()

            # Create new window
            new_window = tk.Toplevel(self.root)
            new_window.title("Generated Graph")
            new_window.geometry("800x600")

            # Wait for window to be created
            new_window.update()

            # Open and resize the image
            img = Image.open(image_path)
            img = img.resize((800, 600), Image.Resampling.LANCZOS)

            # Create PhotoImage after window is ready
            self.photo = ImageTk.PhotoImage(img, master=new_window)

            # Create a Label to display the image
            label = tk.Label(new_window, image=self.photo)
            label.pack()

            # Add a Close Button
            close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
            close_button.pack(pady=10)

        except Exception as e:
            print(f"Error displaying image: {str(e)}")  # Debug print
            messagebox.showerror("Error", f"Failed to display image: {str(e)}")

    def load_json_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                # Load the JSON data and update self.data
                self.data = load_json_data(file_path)
                self.alsolikes = AlsoLikesAnalyzer(self.data)
                data = self.data
                messagebox.showinfo("File Loaded", f"Successfully loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON file: {e}")


def main():
    root = tk.Tk()
    app = MainGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()



