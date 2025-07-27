from flask import Flask, render_template, request, jsonify
#import vertexai
#from vertexai.language_models import ChatModel
import os
import google.generativeai as genai

app = Flask(__name__)
PROJECT_ID = "project-dev-1985"  
LOCATION = "us-central1" 

GOOGLE_API_KEY='AIzaSyBl5oCGT1lAhH_EJsdB2xOCfCOwXd0fwrY'

genai.configure(api_key=GOOGLE_API_KEY)


#vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_session():
    #chat_model = ChatModel.from_pretrained("chat-bison@001")
    generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 20,
                    "max_output_tokens": 1024
                    }
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config)
    chat = model.start_chat()
    return chat

def response(chat, message):
    #parameters = {
     #   "temperature": 0.2,
      #  "max_output_tokens": 256,
       # "top_p": 0.8,
        #"top_k": 40
    #}
    generation_config = {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 20,
                    "max_output_tokens": 1024
                    }
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config)
    #result = chat.send_message(message, **parameters)

    prompt = f"""
        You are a senior story writer. Based on the user's request, 
        suggest potential stories for 200 words.
         the stories should be funny and creative.
        """
    
    result = model.generate_content(prompt)
    #result = chat.send_message(message, generation_config)
    return result.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']
    chat_model = create_session()
    content = response(chat_model,user_input)
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
