import os
import openai

openai.api_key = "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"


code_messages = [
        {'role': "user",
         "content": "You are a polite and helpful coding assistant.  Your main goal is to fix code given to you, based on your knowledge and the error given to you.  Should you encounter a comment in the code and ti begins with the string 'prompt:', interepret the remaining text of the comment as a prompt from the user regarding specific output that should be generated, rather than implicit code completion.  If any changes have been made to the code, the response should end with a list of changes made."}
        ]

box = "code_prompt = I am writing a program, the code looks like this: " + "\n" + code + "\n" + 
    "The error I get looks like this:" + "\n" + error + "\n" + "Can you help me fix my code?"
code_prompt = box

code_messages.append({"role": "user", "content": box})

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=code_messages
)

chat_response = completion.choices[0].message.content

print(completion.choices[0].message.content)
