from flask import Flask, render_template, request
import google.generativeai as genai
import os

app = Flask(__name__)

# Set up the API key (ensure it's correctly set in the environment)
GEMINI_API_KEY = "AIzaSyDp_8PeMI4EHEyF058Fc642f_I7ODDr3xU"  # Or use os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


@app.route('/')
def form():
    return render_template('form.html')  # This is your input form page


@app.route('/submit', methods=['POST'])
def submit():
    # Capture form data
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    previous_history = request.form.get('history')
    previous_medication = request.form.get('medication')
    symptoms = request.form.get('symptoms')

    # Make the API call to generate response from Gemini model
    response = ask_question(
        name=name,
        age=age,
        gender=gender,
        previous_history=previous_history,
        previous_medication=previous_medication,
        symptoms=symptoms
    )

    # Return the response in 'result.html'
    return render_template('result.html', result=response, name=name, age=age, symptoms=symptoms)


def ask_question(name, age, gender, previous_history, previous_medication, symptoms):
    """Use Google Gemini API to get a response based on the user input."""

    # Construct the input prompt
    user_input = f"Patient's Name: {name}, Age: {age}, Gender: {gender}, Previous History: {previous_history}, Previous Medication: {previous_medication}, Symptoms: {symptoms}"

    # Make a request to the Gemini model
    try:
        response = model.generate_content(user_input)
        return response.text  # Extract and return the model's response
    except Exception as e:
        return f"Error generating response: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)

