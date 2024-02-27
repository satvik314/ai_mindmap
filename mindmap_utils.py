from pydantic import BaseModel, Field
from typing import List, Dict
import pyvis
import pyvis.network as net

class MindmapNode(BaseModel):
    title: str = Field(..., description="Title of the node in the mind map.")
    description: str = Field(None, description="Description of the node. If not available, it can be None.")
    children: List['MindmapNode'] = Field([], description="Child nodes of this node. If no children, it can be an empty list.")

class Mindmap(BaseModel):
    title: str = Field(..., description="Title of the mind map.")
    root: MindmapNode = Field(..., description="Root node of the mind map.")


def visualize_interactive_mindmap(mindmap: Mindmap):
    G = net.Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    G.barnes_hut()

    def add_node(node: MindmapNode, parent: str = None):
        G.add_node(node.title, label=node.title, title=node.description)
        if parent:
            G.add_edge(parent, node.title)
        for child in node.children:
            add_node(child, node.title)

    add_node(mindmap.root)

    # Set options for the graph layout
    G.toggle_hide_edges_on_drag(True)
    G.toggle_physics(False)
    G.set_edge_smooth('discrete')

    # Generate and display the HTML for the graph
    html = G.generate_html()
    html = html.replace("'", "\"")

    return f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
    display-capture; encrypted-media;" sandbox="allow-modals allow-forms
    allow-scripts allow-same-origin allow-popups
    allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
    allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""




