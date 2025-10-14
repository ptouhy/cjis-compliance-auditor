from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import PyPDF2
import io

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
    section: str = Form("authenticator")
):
    # Extract text
    if file:
        content = await file.read()
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ''.join([page.extract_text() for page in pdf_reader.pages])
        else:
            text = content.decode('utf-8')
    else:
        text = policy_text
    
    # Run compliance check (simplified for now)
    results = {
        "summary": {
            "total": 5,
            "compliant": 2,
            "nonCompliant": 3,
            "missing": 0,
            "pendingReview": 5
        },
        "checks": []
    }
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)