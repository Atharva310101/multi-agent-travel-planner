# 🤖 Agentic AI Travel Planner

A multi-agent AI system designed to act as a conversational travel assistant. This project leverages the power of Google's Gemini Pro model and the LangChain framework to create a dynamic, step-by-step travel planning experience through a user-friendly chatbot interface.

The system uses an advanced orchestrator-agent architecture to intelligently delegate tasks, manage conversational state, and generate a complete, well-structured travel itinerary from a simple user request.

## 🚀 Live Demo Interaction

Here is an example of a user interacting with the travel planner:

> **You:** Let's plan a trip to Kyoto, Japan.
>
> **AI:** Kyoto is a wonderful choice! To help me plan, what dates are you thinking of traveling?
>
> **You:** How about from April 5th to April 12th for the cherry blossoms?
>
> **AI:** Perfect! A cherry blossom trip to Kyoto from April 5th to 12th. What should we plan first? Flights, hotels, or some activities?
>
> **You:** Let's find a flight.
>
> **AI:** _(After a short pause)_ I've found a plausible flight option for you on Japan Airlines (JAL). The estimated cost is around $1450. Does this sound good?
>
> **You:** Yes, that works. Now find a traditional-style hotel.
>
> **AI:** _(After a short pause)_ For an authentic experience, I suggest the "Kyoto Serenity Ryokan". The estimated price is $280 per night and it has excellent reviews for its traditional atmosphere. Shall we add this to the plan?
>
> **You:** Perfect. Please put it all together in a final itinerary for me.
>
> **AI:** _(After a longer pause, a full itinerary is generated)_
>
> ### 🌸 Your Unforgettable Cherry Blossom Trip to Kyoto 🌸
>
> **Overall Trip Summary**
>
> *   **Destination:** Kyoto, Japan
> *   **Dates:** April 5th - April 12th
> *   **Estimated Total Cost:** ~$3410 (Flight: $1450 + Hotel: $1960)
>
> **Day 1: Arrival in the Ancient Capital**
>
> Welcome to Japan! Your Japan Airlines flight will arrive at Kansai International Airport (KIX). From there, a comfortable train ride will take you to the heart of Kyoto. Check into your traditional lodging, the **Kyoto Serenity Ryokan**, and enjoy a relaxing evening.
> ... _(and so on)_

## 🏛️ Architectural Overview: An Orchestrated System

This project is built on a "manager-worker" multi-agent model, ensuring a robust and intelligent conversational flow.

*   **The Orchestrator Agent (The "Team Leader"):** This is the primary agent the user interacts with. Built with LangChain's `create_tool_calling_agent`, it functions as the central "brain." Its responsibilities are to:
    *   Understand the user's overall travel goal.
    *   Manage the step-by-step conversation.
    *   Ask clarifying questions to gather necessary details (destination, dates).
    *   Intelligently delegate tasks to specialized "worker" agents.
    *   Maintain the overall state of the trip plan.

*   **Specialist Agents (The "Workers"):** These are not full agents but are implemented as powerful **Tools** that the Orchestrator can call upon. Each specialist is a dedicated LangChain chain with a highly-focused prompt, turning Gemini into an expert for a specific task:
    *   `find_flight`: Generates a plausible, fictional flight suggestion.
    *   `find_hotel`: Creates a relevant, fictional hotel suggestion.
    *   `find_activities`: Brainstorms legitimate, famous activities for the destination.
    *   `write_itinerary`: The "reporting agent" that takes the final, structured trip data and composes the beautiful Markdown summary.

*   **The Trip Plan (The Central "Database"):** A simple Python dataclass (`TripState`) acts as the single source of truth for the trip being planned. As the Orchestrator confirms details with the user, it progressively populates this state object.

## 🛠️ Tech Stack

*   **LLM:** Google Gemini Pro (`gemini-1.5-flash-latest`)
*   **Framework:** LangChain (for agent orchestration, prompts, and chains)
*   **UI:** Streamlit (for the interactive web-based chatbot)
*   **Language:** Python 3.9+

## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**2. Create and Activate a Virtual Environment**
```bash
# Create the environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
.\venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Set Up Environment Variables**
*   Create a file named `.env` in the root directory of the project.
*   Open the `.env` file and add your Google Gemini API key:
```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

**5. Run the Streamlit Application**
```bash
streamlit run app.py
```
Your web browser will automatically open with the chatbot interface.

## 🚀 Future Enhancements

*   **Real API Integration:** Replace the AI-generated flight/hotel data with real-time results from APIs like Skyscanner, Amadeus, or Booking.com.
*   **MCP Integration:** Wrap each specialist agent in its own MCP server to make them independently discoverable and interoperable services.
*   **Persistent State:** Store the `TripState` in a database (like SQLite or Firestore) to allow users to resume their planning sessions.
*   **Interactive UI Elements:** Add buttons in the UI for users to explicitly select a flight or hotel option, which would then automatically update the trip state.