# flask app for simple integration with openAI API

from flask import Flask, request, render_template, session, redirect, url_for
from openai import OpenAI
import os


app = Flask(__name__)

app.secret_key = os.urandom(24)

messages = [{"role": "user", "content": "You are a polite and helpful assistant"}]


@app.route('/')
def index():
    if 'api_key' in session:
        return render_template('chat.html')
    else:
        return render_template('api_key.html')


@app.route('/api_key', methods=['POST'])
def set_api_key():
    api_key = request.form['api_key']
    session['api_key'] = api_key
    return redirect(url_for('index'))


@app.route('/chat', methods=['POST'])
def chat():
    api_key = session['api_key']

    client = OpenAI(api_key=api_key)

    model_select = request.form['model-select']

    user_input = request.form['user-input']
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model=model_select,
        messages=messages
        )

    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})

    print(response)
    print("\n")
    print(messages)

    return render_template('chat.html', user_input=user_input, model_select=model_select, messages=messages, response=response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
