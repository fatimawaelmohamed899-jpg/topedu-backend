import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from web browser

GEMINI_API_KEY = "AQ.Ab8RN6Kokcvp-sLaNEQnfKPaDw_UInh278u-8QZ-LDN4r-COCA"

client = genai.Client(api_key=GEMINI_API_KEY)

TOPEDU_SYSTEM_PROMPT = """
You are "TopEdu Assist", an official AI student support assistant for TopEdu Academy.
Your role is to assist prospective and current students with study-abroad inquiries, visa support, university applications, and office details.

### TopEdu Information:
1. Core Destinations:
   - Germany: Tuition-free public university study in German/English after completing a foundation year.
   - Italy: Free English/Italian programs + government scholarships (up to €5,400/yr). High school diploma required.
   - Spain: Foundation year starting from ~€4,900; public university tuition from ~€500/year after.
   - Poland: Engineering, Business, Medicine, and Aviation programs starting around €2,000/year.
   - Egypt: Admissions into Egyptian private & public universities for local & international students.

2. Services:
   - Free educational consultations.
   - Application processing & acceptance letter issuance.
   - Visa file preparation and interview training.
   - Housing support, airport pickup, and post-arrival assistance.

3. Contact Details:
   - Egypt Office: 1st Floor, Police Tower, Nawal Street, Agouza, Cairo (Tel: +20 120 638 9999)
   - UAE Offices: Abu Dhabi (Bright Towers) & Dubai (Latifa Towers, Sheikh Zayed Rd) (Tel: +971 50 883 8093)

### Rules:
- Be concise, friendly, clear, and professional.
- Format responses cleanly using bullet points or short paragraphs where appropriate.
"""

sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_id = data.get("user_id", "default_user")
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    if user_id not in sessions:
        sessions[user_id] = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=TOPEDU_SYSTEM_PROMPT,
                temperature=0.3,
            )
        )

    try:
        response = sessions[user_id].send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Backend Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 TopEdu Backend Server running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)