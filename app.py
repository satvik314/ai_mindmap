from mindmap_utils import *
from phi.assistant import Assistant
from phi.llm.anyscale import Anyscale

import streamlit as st
import streamlit.components.v1 as components

st.title("🧘 Learn through Mindmaps")
st.write("🚀 An interactive mindmap generator powered by AI!")


mindmap_assistant = Assistant(
    llm = Anyscale(model = "mistralai/Mixtral-8x7B-Instruct-v0.1",
                   api_key = st.secrets['ANYSCALE_API_TOKEN']
                   ),
    description = "You create Mindmaps to learn effectively",
    output_model = Mindmap
)

topic = st.text_input("What do you want to learn about?")

if topic:
    mindmap_output = mindmap_assistant.run(topic)
    mindmap_html = visualize_interactive_mindmap(mindmap_output)    
    # st.write(mindmap_html, unsafe_allow_html=True)
    components.html(mindmap_html, height=600)