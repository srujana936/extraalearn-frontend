import streamlit as st
import requests

st.set_page_config(
    page_title="ExtraaLearn Lead Prediction",
    page_icon="🎓",
    layout="centered"
)

BACKEND_URL = (
    "https://extraalearn-backend-service.onrender.com/predict"
)

st.title("ExtraaLearn Lead Conversion Prediction")
st.write(
    "Enter the lead details below to estimate "
    "the likelihood of conversion."
)

with st.form("lead_form"):
    age = st.number_input(
        "Age", min_value=10, max_value=100, value=30
    )

    current_occupation = st.selectbox(
        "Current Occupation",
        ["Professional", "Unemployed", "Student"]
    )

    first_interaction = st.selectbox(
        "First Interaction",
        ["Website", "Mobile App"]
    )

    profile_completed = st.selectbox(
        "Profile Completed",
        ["Low", "Medium", "High"]
    )

    website_visits = st.number_input(
        "Website Visits", min_value=0, value=3
    )

    time_spent_on_website = st.number_input(
        "Time Spent on Website", min_value=0, value=100
    )

    page_views_per_visit = st.number_input(
        "Page Views Per Visit",
        min_value=0.0, value=3.0, step=0.5
    )

    last_activity = st.selectbox(
        "Last Activity",
        ["Email Activity", "Phone Activity", "Website Activity"]
    )

    print_media_type1 = st.selectbox(
        "Newspaper Advertisement", [0, 1]
    )
    print_media_type2 = st.selectbox(
        "Magazine Advertisement", [0, 1]
    )
    digital_media = st.selectbox(
        "Digital Media Advertisement", [0, 1]
    )
    educational_channels = st.selectbox(
        "Educational Channels", [0, 1]
    )
    referral = st.selectbox("Referral", [0, 1])

    submitted = st.form_submit_button("Predict Conversion")

if submitted:
    data = {
        "age": age,
        "current_occupation": current_occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity,
        "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral
    }

    try:
        with st.spinner("Predicting..."):
            response = requests.post(
                BACKEND_URL,
                json=data,
                timeout=120
            )

        if response.ok:
            result = response.json()
            probability = result["conversion_probability"]

            if result["prediction"] == 1:
                st.success("This lead is predicted to be likely to convert.")
            else:
                st.info("This lead is predicted to be less likely to convert.")

            st.metric(
                "Estimated Conversion Probability",
                f"{probability:.2%}"
            )
        else:
            st.error(
                f"Backend error ({response.status_code}): "
                f"{response.text}"
            )

    except requests.RequestException as e:
        st.error(f"Unable to contact the backend: {e}")
