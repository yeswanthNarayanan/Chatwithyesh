import requests

HUGGING_FACE_TOKEN = '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'
API_ENDPOINT = 'https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B-Instruct'

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
    "Content-Type": "application/json"
}

# Sample user input
user_input = "What is the capital of France?"

api_data = {
    "inputs": user_input,
    "parameters": {
        "temperature": 0.7,
        "max_new_tokens": 100
    }
}

response = requests.post(API_ENDPOINT, headers=headers, json=api_data)

if response.status_code == 200:
    api_response = response.json()

    # Check if the response is a list
    if isinstance(api_response, list) and len(api_response) > 0:
        # Access the first item in the list
        generated_text = api_response[0].get("generated_text", "No response generated.")
    else:
        # Handle case when response is a dictionary
        generated_text = api_response.get("generated_text", "No response generated.")
        
    print(generated_text)
else:
    print("Error:", response.status_code, response.json())
