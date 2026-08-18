import boto3
import json

# Create a Bedrock Runtime client
client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

# Prompt
prompt = "Hello LLM! Explain in one sentence what an AI agent is."

# Call the model
response = client.converse(
    modelId="amazon.nova-lite-v1:0",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ]
)

# Extract the response
answer = response["output"]["message"]["content"][0]["text"]

print("User:", prompt)
print("LLM:", answer)