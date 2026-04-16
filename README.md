# CuraMinds Therapeutic Suite: Diagnostic Agent

Welcome to the **CuraMinds Therapeutic Suite**! This platform features a specialized AI-agent designed to rapidly assist with medical diagnosis workflows from radiologist reports and patient vitals. 

Wait times are significantly reduced by ingesting patient records (PDF, TXT) and automating the preliminary assessment, surfacing crucial analytics within seconds instead of weeks. 

## 🩺 Key Features

*   **Multi-Disciplinary Assessment Engine:** Deterministic pipelines tailored for specific therapeutic areas securely extract vitals and match markers for early diagnosis.
*   **Real-time Streaming Interface:** Built using FastAPI WebSockets, the diagnostic steps and agent insights are securely streamed back to the clinician interface dynamically.
*   **Integrated Medical Imaging Check:** Supports referencing and embedding relevant scans (CT Scans, MRIs) based on specific condition trajectories directly in the report UI.
*   **Advanced Clinical Querying:** Interactive clinical chat framework allows clinicians to ask specialized follow-up questions tied to the parsed report (e.g. "What stage could this be and who should I see?").
*   **Plug-and-play Radiologist Module (Aditya Birla MVP):** A decoupled FASTAPI Router specifically leveraging the Open-Weight **Mistral Model** allowing secure standard interfaces into internal hospital EHR systems.
*   **Synthetic Demonstration Readiness:** Comes with highly realistic synthetic reports (`data/`) and medical imaging (`static/images`) to demonstrate workflows on standard edge cases immediately upon setup.

## 🔬 Supported Therapeutic Focus Areas
Based on current data configurations, the demo supports the following diagnostic pathways:
1.  **Lung Cancer:** (e.g., Identifying lung nodules & pulmonary malignancy)
2.  **Breast Cancer:** (e.g., BI-RADS kinetics & imaging correlation)
3.  **Diabetes:** (e.g., Hyperglycemia patterns & HbA1c threshold tracking)
4.  **Hereditary Diseases:** (e.g., Early neurodegenerative markers & caudate atrophy monitoring)

## 🛠 Project Setup

### Prerequisites
- Python 3.9+
- A virtual environment is recommended to containerize dependencies.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CNirhali/CuraMinds_Therapeutic_Suite.git
    cd CuraMinds_Therapeutic_Suite
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate.ps1
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Start the backend analysis server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
Then navigate to `http://127.0.0.1:8000` via your web browser to enter the Agentic Diagnosis Hub.

## 🚀 Running the Demo

1. Open the UI via localhost.
2. In the "Analyze New Report" section, upload any of the `.txt` files located in the `/data` folder (e.g. `lung_cancer_report.txt`).
3. Watch the Agent Hub extract features and process the context into a Final Diagnosis summary.
4. Interact with the chat box beneath the diagnosis to test its advanced follow-up inference context.

---
_Disclaimer: CuraMinds is intended for informational demonstration purposes built upon synthetic environments. It is not currently certified for diagnostic utilization within independent medical ecosystems._