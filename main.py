import streamlit as st
import requests
from datetime import datetime
import toml
secrets = toml.load("C:\Users\ntasa\OneDrive\Pictures\ai ml internship/secrets.toml") 
api_key = "AIzaSyCJXkvjujZGpi75Grcg2qpAu-iZBN-TzCg"

GOOGLE_PLACES_API_KEY = st.secrets["google"]["api_key"]  # Use a secure key

def fetch_travel_suggestions(destination, preferences):
    """Fetch top travel attractions using Google Places API."""
    try:
        query = f"Top attractions in {destination}"
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_PLACES_API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Debugging: Print full API response
        print("API Response:", data)

        if "results" in data:
            return [place["name"] for place in data["results"][:10]]
        else:
            return ["No results found. Try a different location."]
    except Exception as e:
        return [f"Error fetching results: {str(e)}"]

def generate_itinerary(destination, start_date, end_date, preferences):
    days = (end_date - start_date).days + 1
    itinerary = []
    suggestions = fetch_travel_suggestions(destination, preferences)
    
    if not suggestions:
        return "No available suggestions. Try refining your preferences."
    
    for i in range(days):
        day_plan = f"**Day {i+1}:**\n- Morning: {suggestions[i % len(suggestions)]}\n- Afternoon: {suggestions[(i+1) % len(suggestions)]}\n- Evening: {suggestions[(i+2) % len(suggestions)]}"
        itinerary.append(day_plan)
    
    return "\n\n".join(itinerary)

def main():
    st.title("AI-Powered Travel Planner")
    st.write("Personalized travel itinerary based on your preferences.")
    
    # Collect User Inputs
    destination = st.text_input("Where do you want to travel?")
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date", datetime.today())
    budget = st.selectbox("Select Budget", ["Luxury", "Mid-Range", "Budget"])
    preferences = st.multiselect("What are your interests?", ["Sightseeing", "Adventure", "Food", "Culture", "Shopping", "Relaxation"])
    
    if st.button("Generate Itinerary"):
        if destination and start_date and end_date and preferences:
            itinerary = generate_itinerary(destination, start_date, end_date, preferences)
            st.success("Here is your personalized itinerary:")
            st.write(itinerary)
        else:
            st.error("Please provide all required inputs.")

if __name__ == "__main__":
    main()
