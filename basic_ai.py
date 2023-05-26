import os
import openai

openai.api_key = ""


messages = [
  {"role": "user", "content": "You are a polite and helpful assistant"}
  ]

while(True):
    content = input("User:  ")    

    messages.append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content

    print(completion.choices[0].message.content)
