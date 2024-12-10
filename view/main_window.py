import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Document Analytics Application")
        self.root.geometry("1200x800")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frames
        self.input_frame = ttk.LabelFrame(self.root, text="Input Parameters", padding="10")
        self.input_frame.pack(fill="x", padx=10, pady=5)
        
        self.visualization_frame = ttk.LabelFrame(self.root, text="Visualization", padding="10")
        self.visualization_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Input widgets
        # File selection
        ttk.Label(self.input_frame, text="Input File:").grid(row=0, column=0, padx=5, pady=5)
        self.file_path = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Document UUID
        ttk.Label(self.input_frame, text="Document UUID:").grid(row=1, column=0, padx=5, pady=5)
        self.doc_uuid = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.doc_uuid, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # User UUID
        ttk.Label(self.input_frame, text="User UUID:").grid(row=2, column=0, padx=5, pady=5)
        self.user_uuid = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.user_uuid, width=50).grid(row=2, column=1, padx=5, pady=5)
        
        # Analysis options
        self.create_analysis_buttons()
        
        # Results area
        self.create_results_area()
        
    def create_analysis_buttons(self):
        button_frame = ttk.LabelFrame(self.root, text="Analysis Options", padding="10")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="Views by Country", 
                  command=lambda: self.controller.analyze_views_by_country()).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Views by Continent", 
                  command=lambda: self.controller.analyze_views_by_continent()).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Browser Analysis (Detailed)", 
                  command=lambda: self.controller.analyze_browsers_detailed()).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Browser Analysis (Simple)", 
                  command=lambda: self.controller.analyze_browsers_simple()).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Top Readers", 
                  command=lambda: self.controller.analyze_top_readers()).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Also Likes", 
                  command=lambda: self.controller.analyze_also_likes()).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Generate Graph", 
                  command=lambda: self.controller.generate_also_likes_graph()).pack(side="left", padx=5)
        
    def create_results_area(self):
        # Create notebook for different types of results
        self.notebook = ttk.Notebook(self.visualization_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab for histogram plots
        self.plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_frame, text="Plots")
        
        # Tab for text results
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text="Text Results")
        
        self.result_text = tk.Text(self.text_frame, wrap=tk.WORD, height=20)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            
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