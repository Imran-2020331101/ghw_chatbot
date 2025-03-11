# import os, requests, json

GEMINI_API_KEY = 'AIzaSyDIK0AQDNgZBzEaBz8mSYfxO_MhJvFQZrU'
# GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
# headers = {"Content-Type": "application/json"}

# payload = {"prompt":{"text":"Hello, Gemini!"}, "key":GEMINI_API_KEY}
# response = requests.post(GEMINI_API_URL, headers=headers, json=payload )

# print(response.status_code, response.text)


from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents="Hello Gemini"
)
print(response.text)
