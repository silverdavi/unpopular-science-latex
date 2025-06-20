import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

# Data input
data = [
    {"id": "Proto-Indo-European", "parent": None},
    {"id": "Anatolian", "parent": "Proto-Indo-European"},
    {"id": "Hittite", "parent": "Anatolian"},
    {"id": "Luwian", "parent": "Anatolian"},
    {"id": "Tocharian", "parent": "Proto-Indo-European"},
    {"id": "Tocharian A", "parent": "Tocharian"},
    {"id": "Tocharian B", "parent": "Tocharian"},
    {"id": "Italic", "parent": "Proto-Indo-European"},
    {"id": "Latin", "parent": "Italic"},
    {"id": "French", "parent": "Latin"},
    {"id": "Spanish", "parent": "Latin"},
    {"id": "Italian", "parent": "Latin"},
    {"id": "Portuguese", "parent": "Latin"},
    {"id": "Romanian", "parent": "Latin"},
    {"id": "Celtic", "parent": "Proto-Indo-European"},
    {"id": "Goidelic", "parent": "Celtic"},
    {"id": "Irish", "parent": "Goidelic"},
    {"id": "Scottish Gaelic", "parent": "Goidelic"},
    {"id": "Brittonic", "parent": "Celtic"},
    {"id": "Welsh", "parent": "Brittonic"},
    {"id": "Breton", "parent": "Brittonic"},
    {"id": "Germanic", "parent": "Proto-Indo-European"},
    {"id": "West Germanic", "parent": "Germanic"},
    {"id": "English", "parent": "West Germanic"},
    {"id": "German", "parent": "West Germanic"},
    {"id": "Dutch", "parent": "West Germanic"},
    {"id": "North Germanic", "parent": "Germanic"},
    {"id": "Swedish", "parent": "North Germanic"},
    {"id": "Danish", "parent": "North Germanic"},
    {"id": "Norwegian", "parent": "North Germanic"},
    {"id": "Icelandic", "parent": "North Germanic"},
    {"id": "Balto-Slavic", "parent": "Proto-Indo-European"},
    {"id": "Baltic", "parent": "Balto-Slavic"},
    {"id": "Latvian", "parent": "Baltic"},
    {"id": "Lithuanian", "parent": "Baltic"},
    {"id": "Slavic", "parent": "Balto-Slavic"},
    {"id": "East Slavic", "parent": "Slavic"},
    {"id": "Russian", "parent": "East Slavic"},
    {"id": "Ukrainian", "parent": "East Slavic"},
    {"id": "West Slavic", "parent": "Slavic"},
    {"id": "Polish", "parent": "West Slavic"},
    {"id": "Czech", "parent": "West Slavic"},
    {"id": "South Slavic", "parent": "Slavic"},
    {"id": "Serbo-Croatian", "parent": "South Slavic"},
    {"id": "Bulgarian", "parent": "South Slavic"},
    {"id": "Indo-Iranian", "parent": "Proto-Indo-European"},
    {"id": "Indo-Aryan", "parent": "Indo-Iranian"},
    {"id": "Hindi-Urdu", "parent": "Indo-Aryan"},
    {"id": "Bengali", "parent": "Indo-Aryan"},
    {"id": "Punjabi", "parent": "Indo-Aryan"},
    {"id": "Iranian", "parent": "Indo-Iranian"},
    {"id": "Persian", "parent": "Iranian"},
    {"id": "Kurdish", "parent": "Iranian"},
    {"id": "Pashto", "parent": "Iranian"},
    {"id": "Nuristani", "parent": "Indo-Iranian"},
    {"id": "Armenian", "parent": "Proto-Indo-European"},
    {"id": "Greek", "parent": "Proto-Indo-European"},
    {"id": "Ancient Greek", "parent": "Greek"},
    {"id": "Modern Greek", "parent": "Greek"},
    {"id": "Albanian", "parent": "Proto-Indo-European"}
]

# Build the graph
G = nx.DiGraph()
for entry in data:
    if entry["parent"]:
        G.add_edge(entry["parent"], entry["id"])
    else:
        G.add_node(entry["id"])

# Convert to AGraph and configure for tall, narrow layout
A = to_agraph(G)

# Set graph attributes for tall and narrow layout
A.graph_attr.update({
    'rankdir': 'LR',   # Left to right (makes narrow and tall)
    'ranksep': '1.2',  # Tighter horizontal spacing to fit more content
    'nodesep': '0.4',  # Tighter vertical spacing between nodes  
    'size': '6,13.5!', # Set exact paper size: 6" wide by 13.5" tall
    'ratio': 'fill',   # Fill the specified size
    'dpi': '300',      # High resolution
})

# Set node attributes for better appearance
A.node_attr.update({
    'shape': 'box',
    'style': 'rounded,filled',
    'fontname': 'Arial Bold',
    'fontsize': '28',
    'width': '2.0',
    'height': '0.6',
})

# Set edge attributes
A.edge_attr.update({
    'color': '#2C3E50',
    'penwidth': '3.0',
})

# Define vibrant color scheme for major families
family_colors = {
    'Germanic': '#E74C3C',       # Red
    'Celtic': '#27AE60',         # Green  
    'Italic': '#8E44AD',         # Purple
    'Balto-Slavic': '#3498DB',   # Blue
    'Indo-Iranian': '#F39C12',   # Orange
    'Greek': '#16A085',          # Teal
    'Armenian': '#E67E22',       # Dark Orange
    'Albanian': '#95A5A6',       # Gray
    'Anatolian': '#D35400',      # Dark Orange
    'Tocharian': '#9B59B6'       # Light Purple
}

# Special styling for different node types
for node in A.nodes():
    node_name = str(node)
    
    # Root node
    if node_name == "Proto-Indo-European":
        node.attr.update({
            'fillcolor': '#1A252F',
            'fontcolor': 'white',
            'fontsize': '36',
            'style': 'rounded,filled,bold',
            'width': '2.8',
            'height': '0.7',
            'fontname': 'Arial Black'
        })
    # Major language families
    elif node_name in family_colors:
        node.attr.update({
            'fillcolor': family_colors[node_name],
            'fontcolor': 'white',
            'fontsize': '32',
            'style': 'rounded,filled,bold',
            'width': '2.4',
            'height': '0.6',
            'fontname': 'Arial Bold'
        })
    # Intermediate nodes
    elif any(child.startswith(node_name) for child in [n.get_name() for n in A.nodes()]):
        node.attr.update({
            'fillcolor': '#5D6D7E',
            'fontcolor': 'white',
            'fontsize': '30',
            'width': '2.2',
            'height': '0.55',
            'fontname': 'Arial'
        })
    # Leaf nodes (modern languages)
    else:
        node.attr.update({
            'fillcolor': '#ECF0F1',
            'fontcolor': '#2C3E50',
            'fontsize': '28',
            'shape': 'ellipse',
            'width': '2.0',
            'height': '0.5',
            'fontname': 'Arial',
            'style': 'filled'
        })

# Layout the graph
A.layout('dot')

# Save as both SVG and PDF
svg_output_path = "indo_european_tree_tall.svg"
pdf_output_path = "indo_european_tree_tall.pdf"

A.draw(svg_output_path, format='svg')
A.draw(pdf_output_path, format='pdf')

print(f"Generated files:")
print(f"SVG: {svg_output_path}")
print(f"PDF: {pdf_output_path}")
