from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_input = request.form.get("message")

        if "program" in user_input.lower():
            response = "Iron Lady offers leadership, career guidance, and skill development programs."
        elif "process" in user_input.lower():
            response = "Users can explore programs, enroll online, and receive guided mentorship."
        else:
            response = "Ask me about Iron Lady programs or services."

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
