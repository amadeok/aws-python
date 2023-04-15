import os
import openai
k = ""
if os.path.isfile("ooo"):
    with open("ooo", "r")as i:
        d = i.read().splitlines()
        k = d[0]

#openai.api_key = os.getenv("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")
openai.api_key = k

        
response = openai.ChatCompletion.create(
  model = 'gpt-3.5-turbo',
  messages = [
    {'role': 'user', 'content': "what's the easiest way to work with sql in python"}
  ],
  temperature = 0  
)

# response = openai.Completion.create(
#   model="gpt-3.5-turbo",
#   prompt="write some text for a catchy music Tiktok video",
#   temperature=0.7,
#   max_tokens=256,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0
# )
print(response)
print(response["choices"][0]["message"]["content"])
exit()

import openai
import os

# Setup the OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the prompt for the chatbot to start the conversation
prompt = "Hello, how can I assist you today?"

# Define the temperature and max_tokens parameters for the GPT-3 API
temperature = 0.5
max_tokens = 60

# Define a while loop to maintain the chatbot conversation
while True:
    # Get the user's input and append it to the prompt
    user_input = input("User: ")
    prompt += "\nUser: " + user_input

    # Use GPT-3 to generate a response to the user's input
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n = 1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the chatbot's response from the GPT-3 API response
    chatbot_response = response.choices[0].text.strip()

    # Print the chatbot's response and append it to the prompt
    print("Chatbot:", chatbot_response)
    prompt += "\nChatbot: " + chatbot_response