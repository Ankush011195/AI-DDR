import streamlit as st
import os
import tempfile
from pdf_extractor import extract_from_pdf
from claude_engine import generate_ddr
from report_builder import build_ddr_report

st.set_page_config(page_title="DDR Report Generator", layout="centered")
st.title("DDR Report Generator")
st.write("Upload both inspection documents to generate a Detailed Diagnostic Report.")

inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal Report (PDF)", type=["pdf"])

if st.button("Generate DDR Report"):
    if not inspection_file or not thermal_file:
        st.error("Please upload both PDF files first.")
    else:
        with st.spinner("Extracting data from PDFs..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f1:
                f1.write(inspection_file.read())
                inspection_path = f1.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f2:
                f2.write(thermal_file.read())
                thermal_path = f2.name
            inspection_text, inspection_images = extract_from_pdf(
                inspection_path, "extracted_images/inspection"
            )
            thermal_text, thermal_images = extract_from_pdf(
                thermal_path, "extracted_images/thermal"
            )
        with st.spinner("Sending to AI for analysis..."):
            ddr_data = generate_ddr(inspection_text, thermal_text)
        with st.spinner("Building Word document..."):
            os.makedirs("outputs", exist_ok=True)
            output_path = "outputs/DDR_Report.docx"
            build_ddr_report(ddr_data, inspection_images, thermal_images, output_path)
        st.success("Report generated successfully!")
        st.subheader("Report Preview")
        st.write("**Property Issue Summary:**", ddr_data.get("property_issue_summary"))
        st.write("**Severity:**", ddr_data.get("severity_assessment", {}).get("level"))
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download DDR Report (.docx)",
                data=f,
                file_name="DDR_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )