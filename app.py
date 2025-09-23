from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Load schemes dataset
with open("schemefinderdataset.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()
    

    # Handle schemes list request
    if message.lower() == "schemes":
        schemes_list = []
        for i, scheme in enumerate(schemes, 1):
            schemes_list.append({   
                "name": scheme['name'],
                "id": scheme.get('scheme_id', f'S{i:03d}'),
                "benefits": scheme.get("benefits", "N/A"),
                "score": 0,  # No scoring when listing all schemes
                "category": scheme.get("category", "General")
            })
        
        return jsonify({
            "reply": f"Here are all {len(schemes)} schemes available in our database:",
            "type": "schemes",
            "schemes": schemes_list
        })
    
    # Regular chat using GPT
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are SchemeBot, a friendly assistant for Indian government schemes. You have access to {len(schemes)} government schemes in your database. Keep responses concise and helpful. Only refer to schemes that exist in the government database. DO NOT use schemes from data that you have ONLY use schemes from the json file provided to you. Keep your answers concise and to the point. If the user provides some data and none of it really matches the json file do no hesitate to say that there are no available schemes.  If user types 'schemes' just tell all schemes in database. ask for name but not necessary. even if given data doesnt have many inputs for eligbility check the database for the ones given and give the output. your goal is to provide schemes to them but ensure that if data is too vague, you give the scheme but tell that u need more info for accuracy. "},
                {"role": "user", "content": message}
            ],
            max_tokens=500,
        )
        reply = response.choices[0].message.content.strip()
    except:
        reply = f"I'm having some technical difficulties! But I'm here to help you with government schemes. I have {len(schemes)} schemes in my database. Type 'schemes' to see all available schemes!"
    
    return jsonify({
        "reply": reply,
        "type": "normal"
    })

if __name__ == "__main__":
    app.run(debug=True)