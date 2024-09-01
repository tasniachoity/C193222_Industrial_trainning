import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# gro_api_key=os.getenv("GROQ_API_KEY")

def generate_summary(news_body):
    client = Groq()
    chat_completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in summarizing news articles in English. Please summarize the following news article into 3-5 bullet points in English."
            },
            {
                "role": "user",
                "content": news_body
            }
        ],
        temperature=0,
        max_tokens=32768,
        top_p=1,
        stream=False,
        stop=None,
    )
    return chat_completion.choices[0].message.content

    