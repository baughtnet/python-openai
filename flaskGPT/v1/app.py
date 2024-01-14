# flask app for simple integration with openAI API
# imiport libraries
from flask import Flask, request, render_template, session, redirect, url_for
from openai import OpenAI
from html import escape
import markdown
import os
import re

class CodeBlockExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(CodeBlockPreprocessor(md), 'code_block', 25)

class CodeBlockPreprocessor(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        new_lines = []
        in_code_block = False
        language_name = None

        for line in lines:
            if line.startswith("```"):
                if in_code_block:
                    # Close the existing code block
                    new_lines.append("</code></pre>")
                    in_code_block = False
                    language_name = None
                else:
                    # Open a new code block
                    match = re.match(r'^```([a-zA-Z0-9_-]+)', line)
                    if match:
                        language_name = match.group(1)
                        new_lines.append(f'<pre><code class="{language_name}">')
                        in_code_block = True

            elif in_code_block:
                # Add lines inside the code block
                new_lines.append(line)
            else:
                # Add lines outside the code block
                new_lines.append(line)
        return new_lines

# create flask app
app = Flask(__name__)

# set secret key for session management
app.secret_key = os.urandom(24)

# Initialize the messages list
messages = [{"role": "user", "content": "You are a polite and helpful assistant.  Do not reply to this prompt.  It is simply for seting up a base model."}]

def parse_md_with_ext(markdown_text):
    extensions = [CodeBlockExtension()]
    md = markdown.Markdown(extensions=extensions)
    encoded_text = escape(markdown_text)
    html_text = md.convert(encoded_text)
    return html_text

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
    html_content = parse_md_with_ext(response)

    # final_response = md_to_html(response)

    messages.append({"role": "assistant", "content": html_content})

    print(response)
    print("\n")
    print('-------------------------------------')
    print(html_content)

    return render_template('chat.html', user_input=user_input, model_select=model_select, messages=messages, response=response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
