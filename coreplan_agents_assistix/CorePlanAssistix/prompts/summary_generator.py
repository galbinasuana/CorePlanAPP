import os
from openai import OpenAI, OpenAIError

# Creează o instanță a clientului OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # sau setează cheia direct aici dacă nu folosești .env

def generate_section_summary(question, intent, data, section_title=None, example_html=None):
    """
    Generează un rezumat profesionist de la OpenAI pe baza întrebării, intenției și datelor brute.
    Acceptă și un exemplu de structură HTML pentru fine-tuning.
    """
    # Transformăm datele brute într-un text lizibil
    raw_text = ""
    for row in data:
        row_items = [f"{k}: {v}" for k, v in row.items()]
        raw_text += " • " + " | ".join(row_items) + "\n"

    # Mesajele pentru GPT
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional performance analyst tasked with writing executive-level summaries. "
                "You may include advanced insights, bullet points, and HTML formatting such as <b>, <ul>, and <h3>. "
                "You are allowed to include <table> elements if useful to support the insights."
            )
        },
        {
            "role": "user",
            "content": (
                f"Please analyze the following dataset and generate a structured professional summary.\n\n"
                f"### Section Title:\n{section_title or 'Performance Overview'}\n\n"
                f"### Intent:\n{intent}\n\n"
                f"### Example Format:\n{example_html or 'N/A'}\n\n"
                f"### Data:\n{raw_text}"
            )
        }
    ]

    try:
        # Apel API cu noul SDK
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6
        )

        return response.choices[0].message.content

    except OpenAIError as e:
        print(f"❌ GPT Summary Error: {str(e)}")
        return "<i>Could not generate section summary at this time.</i>"
