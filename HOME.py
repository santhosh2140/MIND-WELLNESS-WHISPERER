import json
import uuid
import requests 
import time
import streamlit as st  
from streamlit_lottie import st_lottie
import pyttsx3
import base64
from llama_index.llms.ollama import Ollama
from llama_index.llms import ChatMessage
from st_click_detector import click_detector
from streamlit_extras.add_vertical_space import add_vertical_space 
from llama_index.memory import ChatMemoryBuffer
import threading
from datetime import datetime
import random
import streamlit as st

#for generating the lottie animation.
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
#................................................................................................................
#for strating new convo .........................................................................................
def generate_unique_session_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    random_number = random.randint(1000, 9999)
    return f"{timestamp}{random_number}"

def start_new_chat():
    if st.session_state.messages:
        session_id = str(uuid.uuid4())
        saved_chat = {
            "id": session_id,
            "messages": st.session_state.messages.copy(),   
            "chat_memory": st.session_state.chat_memory.copy(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.stored_chats.append(saved_chat)
    
    st.session_state.messages = []
    st.session_state.interacted = False
    st.session_state.button_clicked = False
    st.session_state.chat_memory = ChatMemoryBuffer.from_defaults(token_limit=5000)
    st.session_state['input'] = ""

#...............................................................................................................
if 'stored_chats' not in st.session_state:
    st.session_state.stored_chats = []


def load_chat(session_id):
    # Find the chat session by its ID
    chat_session = next((chat for chat in st.session_state.stored_chats if chat["id"] == session_id), None)
    if chat_session:
        st.session_state.messages = chat_session["messages"]
        st.session_state.chat_memory = chat_session["chat_memory"]
        st.session_state.interacted = True

for chat_session in st.session_state.stored_chats:
    unique_key = str(uuid.uuid4())

#for Muting the audio fucnction....................................................................................
with st.sidebar:
    AUD=st.toggle("MUTE🔇")
    st.divider() 
#For starting the new chat with new memory state..................................................................
with st.sidebar:
    if st.button('Start New Chat 💬'):
        session_id = generate_unique_session_id()
        
        existing_sessions = [chat for chat in st.session_state.stored_chats if chat["id"] == session_id]
        if not existing_sessions:  # Only append if no existing session with the same ID is found
            new_chat_session = {
                "id": session_id,
                "messages": [],
                "chat_memory": ChatMemoryBuffer.from_defaults(token_limit=5000),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.stored_chats.append(new_chat_session)
            start_new_chat()  
#function to save the text to speech ..............................................................................
def save_text_to_speech(text, file_path):
    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', 1)
    voices = converter.getProperty('voices')
    converter.setProperty('voice', voices[1].id)
    converter.save_to_file(text, file_path)
    converter.runAndWait()
#fucntion to Generate audio............................................................................................
def generate_audio_player(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/x-mpeg;base64,{base64_audio}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """
    return audio_html
#MODEL INIALIZATION..........................................................................................................
llm = Ollama(model="niral1", temperature = 0.5)
chat_memory = ChatMemoryBuffer.from_defaults(token_limit=5000)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.interacted = False

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
#preloading the MODEL ...............................................................................................
lottie_container = st.empty()

if 'model_preloaded' not in st.session_state:
    with lottie_container:
        lottie = load_lottiefile("k.json") 
        st_lottie(
            lottie,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", 
            height=None,
            width=None,
            key=None,
        )
    llm.complete("Hi")
    st.session_state['model_preloaded'] = True
    lottie_container.empty()  

chat_memory = ChatMemoryBuffer.from_defaults()
if 'chat_memory' not in st.session_state:
    st.session_state.chat_memory = ChatMemoryBuffer.from_defaults()

st.title("Mind Wellness Whisperer🧘‍♀️")

question = st.chat_input("Talk with Us")


audio_placeholder = st.empty()

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

button_container = st.empty()
response_container = st.empty()

with st.sidebar:
    with st.expander("Previous Chats🔍"):
        # Ensure that stored_chats is a list and does not contain duplicates
        unique_chats = {chat["id"]: chat for chat in st.session_state.stored_chats}.values()
        for chat_session in unique_chats:
            if st.button(f"Load Chat from {chat_session['timestamp']}", key=chat_session["id"]):
                load_chat(chat_session["id"])
with st.sidebar:
    if st.button('Clear Chat History 🚮 '):
        st.session_state.stored_chats = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if question:
    st.session_state.chat_memory.put(ChatMessage(role="system", content="""You are a listening AI , listen to the user query and answer accordingly .
                                             Instructions to be followed : 
                                                    1. Act only as assistant , not as USER at any cost.
                                                    2.Greet the user well.
                                                    3.When a user concludes the chat by saying "BYE","see you","" anything similar, express gratitude for their interaction.
                                                        """))
    st.session_state.interacted = True
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.chat_memory.put(ChatMessage(role="user", content=question))
    chat_history = st.session_state.chat_memory.get_all() 

    with st.chat_message("assistant"):
        response_container = st.empty()
        assistant_response = llm.stream_chat(chat_history)
        full_response = ''
        for r in assistant_response:
            full_response += r.delta
            
            response_container.write(full_response)
        st.session_state.chat_memory.put(ChatMessage(role="assistant", content=full_response))
        chat_history = st.session_state.chat_memory.get_all() 
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        mp3_file_path = 'response.mp3'
        save_text_to_speech(full_response, mp3_file_path)
        if not AUD:
            audio_player_html = generate_audio_player(mp3_file_path)
            audio_placeholder.markdown(audio_player_html, unsafe_allow_html=True)
        

def button1(msg):
    
    st.session_state.chat_memory.put(ChatMessage(role="system", content="You are Listening Ear AI named LUNA, a personal assistant designed to offer a supportive space for users to express their thoughts and feelings freely. Your role is to listen attentively and provide a non-judgmental, empathetic response, encouraging users to vent about any stresses, frustrations, or challenges they face. Remember to maintain a compassionate tone and offer comfort or general guidance if requested, but focus primarily on allowing the user to speak their mind. Respond directly to the user's expressions and needs without offering unsolicited advice or solutions, unless specifically asked. NOTE = RESPONSE SHOULD BE SHORT  ")),
    st.session_state.chat_memory.put(ChatMessage(role="user", content=just_vent)),
    chat_history = st.session_state.chat_memory.get_all()                             
    response = llm.stream_chat(chat_history)
    return response
def button2(msg):
    
    st.session_state.chat_memory.put(ChatMessage(role="system", content="You are Curiosity Catalyst AI, a personal assistant dedicated to guiding users in their quest for knowledge and learning. Encourage users to explore diverse topics, from academic subjects to new hobbies or skills. Your role is to offer resources, tips, and encouragement tailored to their learning interests. Respond specifically to queries about discovering and engaging with new subjects, providing guidance on how to approach learning effectively and maintain motivation. Remember, your primary goal is to inspire curiosity and make the learning journey enjoyable and accessible for the user. NOTE = RESPONSE SHOULD BE SHORT ")),
    st.session_state.chat_memory.put(ChatMessage(role="user", content=learn_new)),
    chat_history = st.session_state.chat_memory.get_all()                   
    response = llm.stream_chat(chat_history)
    return response
def button3(msg):
    
    st.session_state.chat_memory.put(ChatMessage(role="system", content="You are Heart-to-Heart Helper AI, a personal assistant designed to offer guidance and support in matters of relationships. Encourage users to share their relationship concerns, questions, and experiences. Your role is to provide empathetic, thoughtful, and respectful advice on various aspects of relationships, whether it's about communication, trust, intimacy, or dealing with conflicts. Respond specifically to the relationship-related queries raised by the user, offering insights that help foster understanding, growth, and positive connections in their interpersonal relationships NOTE = RESPONSE SHOULD BE SHORT ")),
    st.session_state.chat_memory.put(ChatMessage(role="user", content=relation_advise)),
    chat_history = st.session_state.chat_memory.get_all()                    
    response = llm.stream_chat(chat_history)
    return response
def button4(msg):
    
    st.session_state.chat_memory.put(ChatMessage(role="system", content="You are Future Pathways AI, a personal assistant dedicated to helping users navigate and shape their future goals and aspirations. Encourage users to discuss their ambitions, dreams, and plans, whether they're related to their career, education, personal life, or financial stability. Your role is to provide guidance, resources, and encouragement tailored to their future planning queries. Respond specifically to questions about goal setting, decision making, long-term planning, and overcoming obstacles, while inspiring confidence and a forward-thinking mindset in the user.")),
    st.session_state.chat_memory.put(ChatMessage(role="user", content=future_plan)),
    chat_history = st.session_state.chat_memory.get_all()
    response = llm.stream_chat(chat_history)
    return response

learn_new = "I want to learn something new."
relation_advise = "Seeking ways to improve communication and trust in a long-distance relationship."
just_vent = "hello i want to vent "
future_plan = "Looking for guidance on setting priorities for career and future."

def handle_button_click(button_id):
    st.session_state.button_clicked = True
    st.session_state.interacted = True
    

    with button_container.empty():
    
        with st.spinner('Thinking🤔💭...'):
            if button_id == 'vent':
                assistant_response = button1(just_vent)
            elif button_id == 'learn':
                assistant_response = button2(learn_new)
            elif button_id == 'advise':
                assistant_response = button3(relation_advise)
            elif button_id == 'future':
                assistant_response = button4(future_plan)
        full_resp = ''
        for r in assistant_response:
            full_resp += r.delta
            response_container.write(full_resp)
        
        st.session_state.messages.append({"role": "assistant", "content": full_resp})
        mp3_file_path = 'response.mp3'
        save_text_to_speech(full_resp, mp3_file_path)
        if not AUD:
                audio_player_html = generate_audio_player(mp3_file_path)
                audio_placeholder.markdown(audio_player_html, unsafe_allow_html=True)
        time.sleep(60)
        st.rerun()

if not st.session_state.interacted and not st.session_state.button_clicked:
    with button_container.container():
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button('Just vent🧮', use_container_width=True):
                            handle_button_click('vent')
                            
                            

                        if st.button('Learn about something new😜', use_container_width=True):
                            handle_button_click('learn')
                            

                    with col2:
                        if st.button('Relationship advise🧘', use_container_width=True):
                            handle_button_click('advise')
                            
                
                        if st.button('Plan for Future🔮', use_container_width=True):
                            handle_button_click('future')
