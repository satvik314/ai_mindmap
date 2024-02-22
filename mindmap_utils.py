from langchain import LLMChain, PromptTemplate
from langchain_openai import OpenAI
from langchain.graphs.networkx_graph import KG_TRIPLE_DELIMITER
from pprint import pprint
from pyvis.network import Network
import networkx as nx
import gradio as gr


# Prompt template for knowledge triple extraction
_DEFAULT_KNOWLEDGE_TRIPLE_EXTRACTION_TEMPLATE = (
    "You are a networked intelligence helping a human track knowledge triples"
    " about all relevant people, things, concepts, etc. and integrating"
    " them with your knowledge stored within your weights"
    " as well as that stored in a knowledge graph."
    " Extract all of the knowledge triples from the text."
    " A knowledge triple is a clause that contains a subject, a predicate,"
    " and an object. The subject is the entity being described,"
    " the predicate is the property of the subject that is being"
    " described, and the object is the value of the property.\n\n"
    "EXAMPLE\n"
    "It's a state in the US. It's also the number 1 producer of gold in the US.\n\n"
    f"Output: (Nevada, is a, state){KG_TRIPLE_DELIMITER}(Nevada, is in, US)"
    f"{KG_TRIPLE_DELIMITER}(Nevada, is the number 1 producer of, gold)\n"
    "END OF EXAMPLE\n\n"
    "EXAMPLE\n"
    "I'm going to the store.\n\n"
    "Output: NONE\n"
    "END OF EXAMPLE\n\n"
    "EXAMPLE\n"
    "Oh huh. I know Descartes likes to drive antique scooters and play the mandolin.\n"
    f"Output: (Descartes, likes to drive, antique scooters){KG_TRIPLE_DELIMITER}(Descartes, plays, mandolin)\n"
    "END OF EXAMPLE\n\n"
    "EXAMPLE\n"
    "{text}"
    "Output:"
)

KNOWLEDGE_TRIPLE_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["text"],
    template=_DEFAULT_KNOWLEDGE_TRIPLE_EXTRACTION_TEMPLATE,
)

llm = OpenAI(temperature = 0.9)

chain = LLMChain(llm = llm, prompt= KNOWLEDGE_TRIPLE_EXTRACTION_PROMPT)

def parse_triples(response, delimiter = KG_TRIPLE_DELIMITER):
  if not response:
    return []
  return response.split(delimiter)

def create_graph_from_triplets(triplets):
  G = nx.DiGraph()
  for triplet in triplets:
    subject, predicate, obj = triplet.strip().split(',')
    G.add_edge(subject.strip(), obj.strip(), label = predicate.strip())
  return G

def nx_to_pyvis(networkx_graph):
    pyvis_graph = Network(notebook=True, cdn_resources='remote')
    for node in networkx_graph.nodes():
        pyvis_graph.add_node(node)
    for edge in networkx_graph.edges(data=True):
        pyvis_graph.add_edge(edge[0], edge[1], label=edge[2]["label"])
    return pyvis_graph

def generateGrapho(pyvis_network):
    # triplets = [t.strip() for t in triples_list if t.strip()]
    # graph = create_graph_from_triplets(triplets)
    # pyvis_network = nx_to_pyvis(graph)

    pyvis_network.toggle_hide_edges_on_drag(True)
    pyvis_network.toggle_physics(False)
    pyvis_network.set_edge_smooth('discrete')

    html = pyvis_network.generate_html()
    html = html.replace("'", "\"")

    return f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
    display-capture; encrypted-media;" sandbox="allow-modals allow-forms
    allow-scripts allow-same-origin allow-popups
    allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
    allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""

def CreateMindmap(text):
  triples = chain.invoke(
                            {'text' : text}
                        ).get('text')
  triples_list = parse_triples(triples)

  networkx_graph = create_graph_from_triplets(triples_list)
  pyvis_network = nx_to_pyvis(networkx_graph)

  pyvis_network.toggle_hide_edges_on_drag(True)
  pyvis_network.toggle_physics(False)
  pyvis_network.set_edge_smooth('discrete')

  html = pyvis_network.generate_html()
  html = html.replace("'", "\"")

  return f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
    display-capture; encrypted-media;" sandbox="allow-modals allow-forms
    allow-scripts allow-same-origin allow-popups
    allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
    allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""