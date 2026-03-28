# AI-DDR Report Generator

An AI-powered system that reads inspection and thermal reports 
and generates a structured Detailed Diagnostic Report (DDR).

## What it does
- Uploads two PDF reports (Inspection + Thermal)
- Extracts text and images from both PDFs
- Uses Groq AI (Llama 3.3 70B) to analyze and merge data
- Generates a structured Word document with 7 sections

## How to run
1. Install dependencies:
   pip install pymupdf python-docx groq streamlit pillow

2. Set API key:
   set GROQ_API_KEY=your_key_here

3. Run the app:
   python -m streamlit run app.py

## Tech Stack
- Python, Streamlit, PyMuPDF, Groq API, python-docx

## Output Sections
1. Property Issue Summary
2. Area-wise Observations with Images
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information
```

**Ctrl+S** save karo. Phir terminal mein:
```
git add README.md
git commit -m "Add README"
git push
