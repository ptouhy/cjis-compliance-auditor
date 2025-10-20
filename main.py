import docx  # Add this line
import io
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
    section: str = Form("authenticator_management")
):
    # --- 1. Extract text ---
    text = ""
    if file:
        content = await file.read() # Read file content as bytes
        
        if file.filename.endswith('.pdf'):
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text = ''.join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
            except Exception as e:
                return {"error": f"Error reading PDF file: {str(e)}"}
        
        # --- NEW: LOGIC TO HANDLE .DOCX FILES ---
        elif file.filename.endswith('.docx'):
            try:
                # Use io.BytesIO to read the byte content as a file
                doc_stream = io.BytesIO(content)
                # Open the document
                doc = docx.Document(doc_stream)
                # Extract text from all paragraphs
                text = '\n'.join([para.text for para in doc.paragraphs if para.text])
            except Exception as e:
                # Catch potential errors from python-docx
                return {"error": f"Error reading .docx file: {str(e)}"}
        # ----------------------------------------

        else:
            # Fallback for plain text files (.txt) or others
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                return {"error": "Uploaded file is not a supported format. Please use .pdf, .docx, or paste text."}

    elif policy_text:
        text = policy_text
    else:
        # Handle error if no text and no file provided
        return {"error": "No policy text or file provided."}

    # Handle cases where text extraction failed or resulted in empty string
    if not text or not text.strip():
        return {"error": "The provided document is empty or text could not be extracted."}
    
    # --- 2. Run the REAL compliance check (This part is unchanged) ---
    try:
        checker = CJISComplianceChecker() #
        compliance_results = checker.check_section(section, text) #
        audit_checklist = checker.generate_audit_checklist(compliance_results) #
        return audit_checklist
    
    except ValueError as e: # Catch unknown section error from checker
        return {"error": str(e)}
    except Exception as e: # Catch any other unexpected errors during analysis
        print(f"Analysis Error: {e}") # Log the full error to the terminal
        return {"error": f"An unexpected error occurred during analysis: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    # Note: The 'reload=True' here is for development.
    # We can also run this from the terminal.
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)