# CJIS Compliance Auditor 🛡️

A full-stack web application that automatically analyzes an agency's security policies against official FBI CJIS standards. Users can paste text or upload a document to generate an instant compliance report that identifies gaps and suggests improvements.

---

## Features

* **Text & File Analysis:** Accepts policy input via direct text paste or PDF file upload.
* **Compliance Reporting:** Systematically checks the policy against known CJIS requirements.
* **Dynamic Results:** Generates a real-time report showing `Compliant`, `Non-Compliant`, and `Missing` items.

---

## Technology Stack

* **Backend:** Python
    * **FastAPI:** For building the web server and API.
    * **Uvicorn:** As the ASGI server to run the application.
    * **PyPDF2:** To extract text from PDF documents.
* **Frontend:**
    * **HTML5:** For page structure.
    * **CSS3:** For all custom styling.
    * **Vanilla JavaScript:** To handle user interactions and API calls (`fetch`).

---

## How to Run This Project Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/cjis-compliance-auditor.git](https://github.com/your-username/cjis-compliance-auditor.git)
    cd cjis-compliance-auditor
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip3 install -r requirements.txt
    ```

4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Open the application in your browser:**
    * Go to `http://127.0.0.1:8000`