import json 
import os 
from typing import Dict
import logging
from google import genai

logger = logging.getLogger()
logger.setLevel(logging.INFO)

GEMINI_API_KEY = 'AIzaSyDIK0AQDNgZBzEaBz8mSYfxO_MhJvFQZrU'
GEMINI_API_URL = 'https://api.gemini.com/v1'


client = genai.Client(api_key={GEMINI_API_KEY})

convo_memory : Dict[str, str] = {}


def chat(query:str, user_id: str) -> Dict[str,str]:
    
    prev_context = convo_memory.get(user_id,'')
    prompt_text = f"{prev_context}\n User:{query}"

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_text,
        )
    except Exception as e:
        logger.error("Gemini Api error: %s",e)
        raise Exception(f"Gemini Api error : {e}")

    bot_response = response.text


    if response.status_code != 200:
        raise ValueError(f"failed to chat with gemini{response.text}")


    if prev_context:
        convo_memory[user_id] = f"{prev_context}\nUser: {query}\nBot: {bot_response}"
    else:
        convo_memory[user_id] = f"User: {query}\nBot: {bot_response}"

    return {"response": bot_response}


def lambda_handler(event, context):
    """
    AWS Lambda handler that expects a JSON body with 'query' and an optional 'user_id'.
    """
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query", "")
        user_id = body.get("user_id", "default_user")

        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Query parameter is missing."}),
                "headers": {"Content-Type": "application/json"}
            }

        result = chat(query, user_id)
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        logger.exception("Error processing the request")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }