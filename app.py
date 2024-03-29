from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    #resp.message("You said: {}".format(msg)).media("https://www.google.co.in/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png")
    text, image = fetch_reply(msg, sender)
    if image=='':
        resp.message(text)
    else:
        resp.message(text).media(image)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)