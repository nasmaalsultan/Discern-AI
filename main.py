from groq import Groq
from flask import Flask, request, render_template, url_for
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key="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",
)

@app.route("/fact-check", methods=["POST"])
def fact_check():
    fact = request.form.get("fact")

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": fact},
            {
                "role": "system",
                "content": """
                    Fact check the user input by returning the line you believe is false
                    whilst providing factual, real, and credible sources that exist to back up your claims.
                    Once you're done, provide an overall percentage of how much of it was false. 
                    Also provide a percentage of your certainty on how correct you are.
                    Please structure your answer for easy readability by ensuring you go to a new line as needed.
                """,
            },
        ],
        model="llama3-8b-8192",
    )

    result = chat_completion.choices[0].message.content
    return render_template("result.html", result=result)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/second")
def second():
    return render_template("second.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("messages.txt", "a") as file:
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Name: {name}\n")
            file.write(f"Email: {email}\n")
            file.write(f"Message: {message}\n")
            file.write("-" * 40 + "\n")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
