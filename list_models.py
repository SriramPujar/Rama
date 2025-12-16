import os
import groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    # Try to grab from Streamlit config if strictly needed, or just warn
    print("GROQ_API_KEY not found in .env")
else:
    client = groq.Groq(api_key=api_key)
    try:
        models = client.models.list()
        print("Available Models:")
        for m in models.data:
            print(f"- {m.id}")
    except Exception as e:
        print(f"Error fetching models: {e}")
