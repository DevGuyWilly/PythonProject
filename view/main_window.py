import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Document Analytics Application")
        self.root.geometry("1200x800")
        
        # Initialize data file path
        self.current_data_file = os.path.join('data', 'sample_100k_lines.json')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frames
        self.create_menu_bar()
        self.create_input_frame()
        self.create_analysis_frame()
        self.create_visualization_frame()
        
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Input Parameters", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Document UUID
        ttk.Label(input_frame, text="Document UUID:").grid(row=0, column=0, padx=5, pady=5)
        self.doc_uuid = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.doc_uuid, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # User UUID
        ttk.Label(input_frame, text="User UUID:").grid(row=1, column=0, padx=5, pady=5)
        self.user_uuid = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.user_uuid, width=50).grid(row=1, column=1, padx=5, pady=5)
        
    def create_analysis_frame(self):
        analysis_frame = ttk.LabelFrame(self.root, text="Analysis Options", padding="10")
        analysis_frame.pack(fill="x", padx=10, pady=5)
        
        # Create buttons for different analyses
        ttk.Button(analysis_frame, text="Views by Country", 
                  command=self.analyze_country_views).pack(side="left", padx=5)
        
        ttk.Button(analysis_frame, text="Views by Continent", 
                  command=self.analyze_continent_views).pack(side="left", padx=5)
        
        ttk.Button(analysis_frame, text="Browser Analysis (Detailed)", 
                  command=self.analyze_browsers_detailed).pack(side="left", padx=5)
        
        ttk.Button(analysis_frame, text="Browser Analysis (Simple)", 
                  command=self.analyze_browsers_simple).pack(side="left", padx=5)
        
        ttk.Button(analysis_frame, text="Top Readers", 
                  command=self.analyze_top_readers).pack(side="left", padx=5)
        
        ttk.Button(analysis_frame, text="Also Likes", 
                  command=self.analyze_also_likes).pack(side="left", padx=5)
        
        ttk.Button(analysis_frame, text="Generate Graph", 
                  command=self.generate_also_likes_graph).pack(side="left", padx=5)
        
    def create_visualization_frame(self):
        self.viz_frame = ttk.LabelFrame(self.root, text="Visualization", padding="10")
        self.viz_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create notebook for different types of results
        self.notebook = ttk.Notebook(self.viz_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab for plots
        self.plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_frame, text="Plots")
        
        # Tab for text results
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text="Text Results")
        
        self.result_text = tk.Text(self.text_frame, wrap=tk.WORD)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def show_plot(self, figure):
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        canvas = FigureCanvasTkAgg(figure, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def show_text_result(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.notebook.select(self.text_frame)
        
    def show_error(self, message):
        messagebox.showerror("Error", message)
        
    def run(self):
        self.root.mainloop() 

    def load_data(self):
        filename = filedialog.askopenfilename(
            initialdir="./data",
            title="Select Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.controller.load_data(filename)
                self.current_data_file = filename
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                self.show_error(f"Error loading data: {str(e)}")

    def analyze_country_views(self):
        doc_id = self.doc_uuid.get()
        if not doc_id:
            self.show_error("Please enter a Document UUID")
            return
        self.controller.analyze_views_by_country(doc_id)
        
    def analyze_continent_views(self):
        doc_id = self.doc_uuid.get()
        if not doc_id:
            self.show_error("Please enter a Document UUID")
            return
        self.controller.analyze_views_by_continent(doc_id)
        
    def analyze_browsers_detailed(self):
        self.controller.analyze_browsers_detailed()
        
    def analyze_browsers_simple(self):
        self.controller.analyze_browsers_simple()
        
    def analyze_top_readers(self):
        self.controller.analyze_top_readers()
        
    def analyze_also_likes(self):
        doc_id = self.doc_uuid.get()
        visitor_id = self.user_uuid.get()
        if not doc_id:
            self.show_error("Please enter a Document UUID")
            return
        self.controller.analyze_also_likes(doc_id, visitor_id if visitor_id else None)
        
    def generate_also_likes_graph(self):
        doc_id = self.doc_uuid.get()
        visitor_id = self.user_uuid.get()
        if not doc_id:
            self.show_error("Please enter a Document UUID")
            return
        self.controller.generate_also_likes_graph(doc_id, visitor_id if visitor_id else None) 