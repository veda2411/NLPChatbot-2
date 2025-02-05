from flask import Flask, render_template, request, session
import uuid

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for session handling

# Function to process text
def process_text(input_text, option):
    if option == "lowercase":
        return input_text.lower()
    elif option == "stopwords":
        stopwords = {'a', 'an', 'the', 'is', 'at', 'of', 'on', 'and', 'in', 'to', 'it'}
        return ' '.join(word for word in input_text.split() if word.lower() not in stopwords)
    elif option == "punctuation":
        import string
        return input_text.translate(str.maketrans('', '', string.punctuation))
    elif option == "swapcase":
        return input_text.swapcase()
    else:
        return "Invalid option"

@app.route("/", methods=["GET", "POST"])
def chat():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())  # Generate unique session ID
        session["chat_history"] = []  # Initialize empty chat history

    if request.method == "POST":
        user_input = request.form["user_input"]
        option = request.form["option"]
        bot_response = process_text(user_input, option)

        
        session["chat_history"].append((user_input, bot_response))
        session.modified = True 

    return render_template("index3.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
