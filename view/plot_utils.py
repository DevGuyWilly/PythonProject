import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def create_bar_plot(data, title, xlabel, ylabel="Count"):
    """Create a matplotlib figure with a bar plot"""
    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    
    # Sort data by values in descending order
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    
    # Create bar plot
    bars = ax.bar(range(len(sorted_data)), list(sorted_data.values()))
    
    # Customize the plot
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # Set x-axis labels
    ax.set_xticks(range(len(sorted_data)))
    ax.set_xticklabels(sorted_data.keys(), rotation=45, ha='right')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    # Adjust layout to prevent label cutoff
    fig.tight_layout()
    
    return fig 