import streamlit as st
import json
import os
from scraper import get_swiggy_results

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
    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            color: #FF6347;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #FF6347;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🍽️ Smart Food Recommender</div>', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/135/135620.png", width=100)
    st.subheader("👤 New User Registration")

    with st.form("registration_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        state = st.text_input("State")
        city = st.text_input("City")
        pin_code = st.text_input("Pin Code")

        allergy_options = ["Gluten", "Peanuts", "Dairy", "Soy", "Shellfish", "Eggs"]
        allergies = st.multiselect("Food Allergies", allergy_options)

        submitted = st.form_submit_button("Register")
        if submitted:
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
            st.success("🎉 Registered successfully!")
            st.balloons()
            st.experimental_rerun()

# Search & Recommendation Page
def recommendation_page(user):
    st.markdown("""
    <style>
        .search-title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #20B2AA;
        }
        .food-card {
            background-color: #F0F8FF;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="search-title">🔍 Search for Restaurants, Food or Brands</div>', unsafe_allow_html=True)
    query = st.text_input("Search for food, drinks, or brands")

    if query:
        with st.spinner("Fetching recommendations from Swiggy..."):
            results = get_recommendations(query, user)
            if results:
                for item in results:
                    st.markdown(f"""
                    <div class="food-card">
                        <strong>{item['name']}</strong><br>
                        📍 {item['location']}<br>
                        💰 {item['price']}<br>
                        ⭐ {item['rating']}<br>
                        🔗 <a href="{item['url']}" target="_blank">View</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No matching results found.")

# Swiggy-Based Recommendation Engine
def get_recommendations(query, user):
    allergy_filter = user["allergies"]
    pin = user["pin_code"]

    all_results = get_swiggy_results(query, pin)

    # Basic allergy filter (e.g., skip if "gluten" found in name and user has gluten allergy)
    filtered = []
    for item in all_results:
        name_lower = item["name"].lower()
        if any(allergy in name_lower for allergy in allergy_filter):
            continue
        filtered.append(item)

    return filtered or all_results

# App Entry Point
def main():
    st.set_page_config(page_title="Smart Food Recommender", layout="wide")

    if "user" not in st.session_state:
        registration_page()
    else:
        recommendation_page(st.session_state.user)

if __name__ == "__main__":
    main()
