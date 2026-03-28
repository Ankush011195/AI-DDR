import os
import json
from groq import Groq

def generate_ddr(inspection_text, thermal_text):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""You are a professional building diagnostics expert. You have been given raw data from two inspection reports. Your job is to produce a structured DDR (Detailed Diagnostic Report) that is clear, professional, and client-friendly.

INSPECTION REPORT DATA:
{inspection_text}

THERMAL REPORT DATA:
{thermal_text}

STRICT RULES:
- Do NOT invent any facts not present in the documents
- If information is missing, write exactly: "Not Available"
- If information conflicts between the two documents, write the conflict clearly
- Use simple, non-technical language that any client can understand
- Do not use jargon

Return your response as a valid JSON object with EXACTLY these 7 keys:
{{
  "property_issue_summary": "A short 2-3 sentence overview of the main problems found",
  "area_wise_observations": [
    {{
      "area": "Name of the area/location",
      "observation": "What was found there",
      "thermal_finding": "What the thermal report says about this area, or Not Available",
      "image_hint": "Describe what image from the documents belongs here, or Not Available"
    }}
  ],
  "probable_root_cause": "Explain the likely underlying causes of the issues found",
  "severity_assessment": {{
    "level": "High / Medium / Low",
    "reasoning": "Why this severity level was assigned"
  }},
  "recommended_actions": [
    "Action 1",
    "Action 2"
  ],
  "additional_notes": "Any other relevant observations or context",
  "missing_or_unclear_information": "List anything that was unclear, missing, or conflicting in the source documents. Write Not Available if everything was clear."
}}

Return ONLY the JSON object. No explanation before or after it."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )
    
    raw_response = response.choices[0].message.content.strip()
    
    if raw_response.startswith("```"):
        raw_response = raw_response.split("```")[1]
        if raw_response.startswith("json"):
            raw_response = raw_response[4:]
    
    raw_response = raw_response.strip()
    ddr_data = json.loads(raw_response)
    return ddr_data