import json 
import os 
import requests
from typing import Dict
import logging
from google import genai

logger = logging.getLogger()
logger.setLevel(logging.INFO)

GEMINI_API_KEY = 'AIzaSyDIK0AQDNgZBzEaBz8mSYfxO_MhJvFQZrU'
GEMINI_API_URL = 'https://api.gemini.com/v1'


client = genai.Client(api_key={GEMINI_API_KEY})

convo_memory : Dict[str, str] = {}


def chat(query:str, user_id: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("Gemini api key not set")

    headers = {"Content-Type": "application/json"}
    prev_context = convo_memory.get(user_id,'')
    prompt_text = f"{prev_context}\n User:{query}"

    payload = {"prompt": prompt_text, "max_tokens":100, "temparature": 0.5}
    response = requests.post( f"{GEMINI_API_URL}/chat", headers=headers, json=payload )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt_text,
    )

    print(response.text)


    if response.status_code != 200:
        raise ValueError(f"failed to chat with gemini{response.text}")


    response_data = response.json()
    bot_response = response_data.get('choices',[{}])[0].get('text','')
    convo_memory[user_id] = f"{prev_context} \nUser:{query}\nBot:{bot_response}"

    return bot_response



def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        query = body['query']
        user_id = body['user_id']

        if not query:
            raise ValueError('Query is required')
        
        result = chat(query,user_id)
        return {
            'statusCode':200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode' : 500,
            'body' : json.dumps(str(e))
        }