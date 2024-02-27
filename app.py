from mindmap_utils import *
from phi.assistant import Assistant
from phi.llm.anyscale import Anyscale


import streamlit as st
import streamlit.components.v1 as components

import supabase
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
db_client = supabase.create_client(supabase_url, supabase_key)   


st.title("🧘 Learn through Mindmaps")
st.write("🚀 An interactive mindmap generator powered by AI!")
st.markdown("""
- Created by Build Fast with AI. Join the [Community](https://chat.whatsapp.com/BmE9HoWQ3irKt9gG8LshGX).        
""")


mindmap_assistant = Assistant(
    llm = Anyscale(model = "mistralai/Mixtral-8x7B-Instruct-v0.1",
                   api_key = st.secrets['ANYSCALE_API_TOKEN']
                   ),
    description = "You create Mindmaps to learn effectively",
    output_model = Mindmap
)

topic = st.text_input("What do you want to learn about?")

placeholder = st.empty()

with placeholder.container():
   st.code("""
            Try:
            String Theory
            Concept of Dualism
            """, language= None)

if topic:
    mindmap_output = mindmap_assistant.run(topic)
    db_client.table("mindmap_db").insert({
        "topic": topic,
        "mindmap": str(mindmap_output)
    }).execute()
    mindmap_html = visualize_interactive_mindmap(mindmap_output)    
    # st.write(mindmap_html, unsafe_allow_html=True)
    components.html(mindmap_html, height=600)