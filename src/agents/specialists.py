from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import tool
from .prompts import FLIGHT_PROMPT, HOTEL_PROMPT, ACTIVITIES_PROMPT, ITINERARY_WRITER_PROMPT
import json

from dotenv import load_dotenv # <-- ADD THIS LINE
load_dotenv() # <-- AND ADD THIS LINE

# Initialize the LLM once to be reused by all specialists
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.8)

@tool
def find_flight(destination: str, start_date: str, end_date: str) -> dict:
    """Finds a flight for the given trip details. Returns JSON."""
    prompt = PromptTemplate.from_template(FLIGHT_PROMPT)
    chain = prompt | llm | JsonOutputParser()
    return chain.invoke({"destination": destination, "start_date": start_date, "end_date": end_date})

@tool
def find_hotel(destination: str, start_date: str, end_date: str) -> dict:
    """Finds a hotel for the given trip details. Returns JSON."""
    prompt = PromptTemplate.from_template(HOTEL_PROMPT)
    chain = prompt | llm | JsonOutputParser()
    return chain.invoke({"destination": destination, "start_date": start_date, "end_date": end_date})

@tool
def find_activities(destination: str) -> dict:
    """Finds activities for the given destination. Returns JSON."""
    prompt = PromptTemplate.from_template(ACTIVITIES_PROMPT)
    chain = prompt | llm | JsonOutputParser()
    return chain.invoke({"destination": destination})

@tool
def write_itinerary(trip_state: str) -> str:
    """Takes a JSON string of the trip state and writes a full itinerary."""
    prompt = PromptTemplate.from_template(ITINERARY_WRITER_PROMPT)
    chain = prompt | llm
    response = chain.invoke({"trip_state": trip_state})
    return response.content