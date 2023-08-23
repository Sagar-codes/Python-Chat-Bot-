import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    load_dotenv()
    #Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

def main():
    init()

    chat = ChatOpenAI(temperature=0) # temparature is to repond with different message when it is set to 1, now it is 0 to cache previous question by human.

    if "messages" not in st.session_state: # setting up a state for messages
        st.session_state.messages = [
            SystemMessage(content="You are a helpfull assitant."),
        ]

    st.set_page_config(
        page_title="Python ChatBot",
        page_icon="🤖"
    )

    st.header("Your Own ChatBot 🤖")

    # message("Hello How Are You")
    # message("Hello How Are You", is_user=True)

    with st.sidebar:
        user_input = st.text_input("Your Message: ", key='user_input')

        if user_input: # When a user submits a input
            # message(user_input, is_user=True) # Showing Human Message in the chat
            st.session_state.messages.append(HumanMessage(content=user_input)) # append human messages to messages history
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages) # send the message history to openAI
            st.session_state.messages.append(AIMessage(content=response.content))
            # message(response.content, is_user=False) # and show the reponse in AI message


    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')






if __name__ == '__main__':
    main()