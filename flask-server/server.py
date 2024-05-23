from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Your Gemini API key
GEMINI_API_KEY = 'AIzaSyCclRMJ0cdftV0xAhHS7yPEyMWbc3TZtPs'

products_schema = [
    {
        "Product_name": "Eco-friendly Water Bottle",
        "Product_description": "A reusable water bottle made from stainless steel, featuring double-wall insulation to keep beverages hot or cold for hours.",
        "Reason": "Chosen for its environmental benefits and the growing consumer preference for sustainable products."
    },
    # Add other products here...
]

# Initialize the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')

@app.route('/generate_gift_idea', methods=['POST'])
def generate_gift_idea():
    data = request.json
    age = data.get('age')
    gender = data.get('gender')
    occasion = data.get('occasion')
    recipient_type = data.get('recipient_type')
    prompt = f"You have a very good choice, so just provide me a list of 12 highly-rated and trending different gift ideas for a {age}-year-old {recipient_type} who is {gender} and loves electronic items. These gifts should be suitable for {occasion} and available on Amazon India. Ensure that each product followed by only its product_names, description of each product, each product followed by its description and a convincing reason for its selection and ensure that product are listed without any special characters such as *, here{products_schema} is an example with three products with its Product_name:, Description:, Reason_for_selection :, similarly do that for all 12 product."
    
    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        gift_ideas = process_text_for_gift_ideas(generated_text)[:12]
        return jsonify({"gift_ideas": gift_ideas})
    except Exception as e:
        print(f"Error generating gift ideas: {e}")
        return jsonify({"error": "Error generating gift ideas"}), 500

@app.route('/search_gift_idea', methods=['POST'])
def search_gift_idea():
    data = request.json
    textdata = data.get('prompt')
    prompt = f"Task: Gift idea generation\nDescription: Based on {textdata} generate gift idea suggestions that are available on Amazon India ecommerce website. Ensure that only the product names, descriptions, and reason is provided as example in schema {products_schema}. Additionally, include each product followed by its description and a convincing reason for its selection. Provide me the output in the format:\nProduct:\nDescription:\nReason:"

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        gift_ideas = process_text_for_gift_ideas(generated_text)[:12]
        return jsonify({"gift_ideas": gift_ideas})
    except Exception as e:
        print(f"Error generating gift ideas: {e}")
        return jsonify({"error": "Error generating gift ideas"}), 500

def process_text_for_gift_ideas(text):
    return text.split('\n')[:12]

if __name__ == '__main__':
    app.run(debug=True)
