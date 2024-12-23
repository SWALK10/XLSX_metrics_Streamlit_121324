import os

api_key = os.environ.get("OPENAI_API_KEY")

if api_key:
    print("OPENAI_API_KEY is set:", api_key[:4] + "***" + api_key[-4:]) # Shows first and last 4 chars to confirm
else:
    print("OPENAI_API_KEY is NOT set.")