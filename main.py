from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import PyPDF2
import io

# --- NEW: Import the "brain" ---
from compliance_checker import CJISComplianceChecker, ComplianceStatus

app = FastAPI(title="CJIS Compliance Auditor")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/analyze")
async def analyze_policy(
    file: UploadFile = File(None),
    policy_text: str = Form(None),
    section: str = Form("authenticator_management") # Changed default
):
    # --- 1. Extract text (This logic is the same) ---
    text = ""
    if file:
        content = await file.read()
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ''.join([page.extract_text() for page in pdf_reader.pages])
        else:
            text = content.decode('utf-8')
    elif policy_text:
        text = policy_text
    else:
        # Handle error if no text is provided
        return {"error": "No policy text or file provided."}

    if not text.strip():
        # Handle error for empty or unreadable file
        return {"error": "The provided document is empty or could not be read."}
    
    # --- 2. Run the REAL compliance check (This replaces the placeholder) ---
    try:
        # Create an instance of the "brain"
        checker = CJISComplianceChecker()
        
        # Run the analysis using the extracted text and section
        compliance_results = checker.check_section(section, text)
        
        # Format the results into a clean checklist for the frontend
        audit_checklist = checker.generate_audit_checklist(compliance_results)
        
        # Send the REAL results back
        return audit_checklist
    
    except ValueError as e:
        # This catches if the section name is invalid
        return {"error": str(e)}
    except Exception as e:
        # This catches any other unexpected errors
        return {"error": f"An unexpected error occurred: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    # Note: The 'reload=True' here is for development.
    # We can also run this from the terminal.
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)