import asyncio
import random
import time
import json

class AgentEngine:
    def __init__(self):
        pass

    async def analyze_report(self, filename: str, content_size: int):
        yield f"Agent Initialized. Receiving report: {filename} ({content_size} bytes)"
        await asyncio.sleep(0.5)

        yield "Parsing medical report format..."
        await asyncio.sleep(0.5)
        
        if "lung" in filename.lower():
            yield "Extracting pulmonary metrics and cross-referencing CT scans..."
            await asyncio.sleep(0.5)
            yield "Identifying specific nodule characteristics in right upper lobe..."
            final_report = "--- FINAL DIAGNOSIS SUMMARY ---\nDetected 2.4 cm speculated nodule in the right upper lobe.\nSuspicion: Primary pulmonary malignancy (Early Stage).\nRecommendation: Schedule immediate consultation with Thoracic Oncology."
            image_ref = "lung_ct.png"
        elif "breast" in filename.lower():
            yield "Extracting MRI kinetic curves..."
            await asyncio.sleep(0.5)
            yield "BI-RADS categorization in progress..."
            final_report = "--- FINAL DIAGNOSIS SUMMARY ---\nDetected 1.8 cm distinct mass in right breast with Type II kinetics.\nSuspicion: BI-RADS Category 4. Suspicious abnormality.\nRecommendation: Core needle biopsy required. Book Breast Surgical Oncologist."
            image_ref = "breast_mri.png"
        elif "diab" in filename.lower():
            yield "Analyzing metabolic panels and tracking hyperglycemia indicators..."
            await asyncio.sleep(0.5)
            yield "Correlating HbA1c with presenting symptomatic fatigue..."
            final_report = "--- FINAL DIAGNOSIS SUMMARY ---\nFasting Glucose: 215 mg/dL. HbA1c: 8.4%.\nDiagnosis: Diabetes Mellitus.\nRecommendation: Immediate insulin regulation therapy and endocrinologist visit."
            image_ref = "none"
        elif "hered" in filename.lower():
            yield "Cross-referencing genetic markers and neurology imaging..."
            await asyncio.sleep(0.5)
            yield "Checking for bilateral caudate atrophy related to HD..."
            final_report = "--- FINAL DIAGNOSIS SUMMARY ---\nMild neurodegenerative markers found on MRI, consistent with family history.\nDiagnosis: Early manifestations of suspected hereditary neurodegeneration.\nRecommendation: Neurology consult for CAG repeat expansion test."
            image_ref = "brain_mri.png"
        else:
            yield "Analyzing general biomarkers..."
            await asyncio.sleep(0.5)
            final_report = "--- FINAL DIAGNOSIS SUMMARY ---\nNo specific severe anomalies detected. Normal vitals.\nRecommendation: Standard annual follow-up."
            image_ref = "none"

        await asyncio.sleep(0.5)
        # We yield a JSON string for the final output so the client can pick up the image reference
        yield json.dumps({"text": final_report, "image": image_ref})

    async def answer_query(self, filename: str, query: str):
        query = query.lower()
        await asyncio.sleep(0.3)
        if "lung" in filename.lower():
            if "special" in query or "who" in query or "doctor" in query:
                response = "Based on the right upper lobe nodule, you should consult a **Thoracic Oncologist** and an **Interventional Pulmonologist** for a biopsy."
            elif "surviv" in query or "stage" in query:
                response = "The 2.4 cm size without significant lymph node spread on the CT suggests Stage I or Stage II. Early detection greatly improves outcomes (5-year survival > 70% typically for early stage), but staging requires biopsy confirmation."
            else:
                response = "I have cross-referenced the lung CT. The immediate priority is confirming the nature of the 2.4cm nodule via biopsy."
        elif "breast" in filename.lower():
            if "special" in query or "doctor" in query:
                response = "You should schedule an appointment with a **Breast Surgical Oncologist** immediately to discuss biopsy options for the BI-RADS 4 lesion."
            elif "bi-rad" in query or "category 4" in query:
                response = "BI-RADS Category 4 means the finding is suspicious for malignancy (2% to 94% chance). A biopsy is mandatory to determine if it is indeed cancer."
            else:
                response = "Based on the MRI, the Type II kinetic curve in the 1.8cm lesion warrants further invasive testing to verify cellular morphology."
        elif "diab" in filename.lower():
            if "diet" in query or "food" in query:
                response = "Given an HbA1c of 8.4%, strict carbohydrate management, high fiber intake, and the elimination of refined sugars are essential alongside your insulin therapy."
            elif "special" in query or "doctor" in query:
                response = "An **Endocrinologist** is the primary medical specialist you need to see, along with a certified **Diabetes Educator**."
            else:
                response = "Your glucose levels (215 mg/dL) are critically elevated. Immediate adherence to medication is advised to prevent ketoacidosis."
        elif "hered" in filename.lower():
            if "special" in query or "doctor" in query:
                response = "A **Neurologist specializing in Movement Disorders** or Neurogenetics, along with a **Genetic Counselor**, are the recommended specialists."
            elif "hd" in query or "huntington" in query:
                response = "Given the family history and caudate atrophy shown on the MRI, Huntington's Disease is a primary differential diagnosis. A CAG repeat genetic expansion test is conclusive."
            else:
                response = "We observed mild ventricular prominence and caudate atrophy on the MRI, typical of certain hereditary neurodegenerative conditions."
        else:
            response = "I can analyze context from the specific reports. For general questions, I recommend consulting a General Practitioner."

        # simulated stream
        words = response.split(' ')
        for i, word in enumerate(words):
            yield word + (" " if i < len(words)-1 else "")
            await asyncio.sleep(0.02)
