import sys
import os
import json
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Path fix

# --- NEW: Suppress noisy gRPC/ALTS informational warnings ---
# Get the specific loggers and set their level to a higher one (like ERROR)
# This will hide the INFO-level "ALTS creds ignored" messages.
logging.getLogger('google.api_core.bidi').setLevel(logging.ERROR)
logging.getLogger('google.auth.transport.requests').setLevel(logging.ERROR)
# --- End of Fix ---


import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.core.state import TripState
from src.agents.specialists import find_flight, find_hotel, find_activities, write_itinerary

# --- CONFIGURATION ---
load_dotenv()
st.set_page_config(page_title="Multi-Agent Travel Planner", page_icon="✈️", layout="wide")

# --- AGENT SETUP ---
# This is the "Team Leader" or Orchestrator Agent
@st.cache_resource
def create_orchestrator_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5)
    tools = [find_flight, find_hotel, find_activities, write_itinerary]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the master travel planner orchestrator.
        Your job is to manage a conversation with a user to plan their trip step-by-step.
        
        Here is the process:
        1.  First, you MUST get the user's destination, start date, and end date. If any are missing, ask for them.
        2.  Once you have the core details, confirm them with the user.
        3.  Then, ask the user what they want to plan next: flights, hotels, or activities.
        4.  Use the appropriate tool to find options for them.
        5.  Present the options to the user. Allow them to confirm a choice.
        6.  Once the user is happy with all the parts of their trip, they will ask for the final itinerary.
        7.  Use the `write_itinerary` tool ONLY when the user asks for the final summary. You will need to pass the complete trip state to it.
        
        IMPORTANT: Do not call multiple tools at once. Plan one part of the trip at a time, conversationally."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- STREAMLIT APP ---
st.title("🤖 Multi-Agent Travel Planner")

# Initialize session state for chat history and trip state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your AI travel planner. Where would you like to go?"}]
if "trip_state" not in st.session_state:
    st.session_state.trip_state = TripState()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

orchestrator = create_orchestrator_agent()

# Handle user input
if prompt := st.chat_input("Your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 The agents are collaborating..."):
            # Prepare agent input
            agent_input = {
                "input": prompt,
                "chat_history": st.session_state.messages,
                # We pass the current state in the prompt, so the agent is aware of it
                "current_plan": json.dumps(st.session_state.trip_state.to_dict(), indent=2)
            }

            # Invoke the orchestrator agent
            result = orchestrator.invoke(agent_input)
            response = result["output"]

            # NOTE: A more advanced version would have the agent's tool calls
            # automatically update the st.session_state.trip_state.
            # For now, we will do it manually in the chat if needed.
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})