import streamlit as st
from groq import Groq
import os


st.set_page_config(page_title="AI Study Planner")

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(" API Key not found.")
    st.stop()

client = Groq(
    api_key=api_key
)


st.title("AI Study Planner")

goal = st.text_input("Enter your Goal")

days = st.number_input("How many days you are planning", 1, 366, 30)
hours = st.number_input("Study hours per day", 1, 24, 2)
desc = st.text_area("About your goal", height=100)


if st.button("Generate Study Plan"):

    if not goal:
        st.warning(" Please enter a goal")
        st.stop()

    prompt = f"""
    Create a detailed {days}-day study plan.

    Goal: {goal}
    Study hours per day: {hours}
    Description: {desc}

    Instructions:
    - Divide topics day-wise
    - Keep it simple and structured
    - Include revision days
    - Add small milestones
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful study planner."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        st.success(" Plan Generated Successfully!")
        st.write(result)

    except Exception as e:
        st.error(f" Error: {e}")
