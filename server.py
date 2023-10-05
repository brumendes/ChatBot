import sys
from flask import Flask
from flask_cors import cross_origin
from evaluation import chatbot_response


app = Flask(__name__)

@app.route("/<input>")
@cross_origin()
def response(input): 
    print(input)   
    return chatbot_response(input)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)