import streamlit as st
import json
import os
from scraper import get_swiggy_results  # Make sure this function is defined properly

# File to store user data
USER_DATA_FILE = "users.json"

# Load existing users
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user
def save_user(user):
    users = load_users()
    users[user["name"]] = user
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Registration page
def registration_page():
    st.title("New User Registration")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    state = st.text_input("State")
    city = st.text_input("City")
    pin_code = st.text_input("Pin Code")

    allergy_options = ["Gluten", "Peanuts", "Dairy", "Soy", "Shellfish", "Eggs"]
    allergies = st.multiselect("Food Allergies", allergy_options)

    if st.button("Register"):
        if not name or not state or not city or not pin_code:
            st.error("Please fill all the required fields.")
        else:
            user = {
                "name": name,
                "age": age,
                "gender": gender,
                "state": state,
                "city": city,
                "pin_code": pin_code,
                "allergies": [a.strip().lower() for a in allergies],
            }
            save_user(user)
            st.session_state.user = user
            st.success("Registered successfully!")
            st.rerun()

# Login page
def login_page():
    st.title("User Login")
    name = st.text_input("Enter your name")
    if st.button("Login"):
        users = load_users()
        if name in users:
            st.session_state.user = users[name]
            st.success(f"Welcome back, {name}!")
            st.rerun()
        else:
            st.error("User not found. Please register.")

# Recommendation Page
def recommendation_page(user):
    st.title("Search Restaurants and Food")

    st.sidebar.markdown(f"""
    **Logged in as:** {user['name']}  
    📍 {user['city']}, {user['state']}  
    ⚠️ Allergies: {", ".join(user['allergies']).title() or "None"}
    """)

    query = st.text_input("Search for food, drinks, or brands")

    if query:
        with st.spinner("Fetching recommendations from Swiggy..."):
            try:
                results = get_recommendations(query, user)
                if results:
                    st.subheader(f"Results for '{query}':")
                    for item in results:
                        st.markdown(f"""
                        **{item['name']}**  
                        📍 {item['location']}  
                        💰 {item['price']}  
                        ⭐ {item['rating']}  
                        🔗 [View]({item['url']})
                        ---
                        """)
                else:
                    st.warning("No safe results found based on your allergy preferences.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Recommendation Engine
def get_recommendations(query, user):
    allergy_filter = user["allergies"]
    pin = user["pin_code"]

    all_results = get_swiggy_results(query, pin)

    filtered = []
    for item in all_results:
        name_lower = item["name"].lower()
        desc = item.get("description", "").lower()
        if any(allergy in name_lower or allergy in desc for allergy in allergy_filter):
            continue
        filtered.append(item)

    return filtered or all_results

# App Entry Point
def main():
    st.set_page_config(page_title="Smart Food Recommender", layout="wide")

    if "user" not in st.session_state:
        option = st.sidebar.selectbox("Choose Action", ["Login", "Register"])
        if option == "Login":
            login_page()
        else:
            registration_page()
    else:
        recommendation_page(st.session_state.user)

if __name__ == "__main__":
    main()
