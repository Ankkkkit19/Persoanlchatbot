from flask import Flask, render_template, request
from chatbot import get_response

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    user = ""
    reply = ""

    if request.method == "POST":
        user = request.form.get("msg")
        reply = get_response(user)

    return render_template("index.html", user=user, reply=reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
