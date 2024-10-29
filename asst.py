import openai

openai.api_key = ""
asst_id = ""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hello, how can I use OpenAI's API?"}
    ]
)

print(response['choices'][0]['message']['content'])