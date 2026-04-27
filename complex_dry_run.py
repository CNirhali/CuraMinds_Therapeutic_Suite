import asyncio
import json
import os
import time

# We mock the Mistral integration to guarantee a reliable and impressive dry run presentation
class MockRadiologistAI:
    def __init__(self):
        self.scenarios = {
            "lung_cancer": {
                "steps": [
                    "Observation 1: Irregular, spiculated opacity in the right upper lobe.",
                    "Observation 2: Positive correlation with chronic cough and smoking history.",
                    "Conclusion: High probability of advanced primary lung carcinoma."
                ],
                "summary": "--- RADIOLOGIST FINDINGS SUMMARY ---\nPatient exhibits a highly suspicious irregular spiculated mass in the RUL measuring 3.5cm. Findings are highly concerning for malignancy. \n\nDifferential Diagnosis: Primary Lung Carcinoma, Granulomatous disease (less likely).",
                "image": "case1_lung_cancer.png",
                "query_resp": "The spiculation indicates desmoplastic reaction typical of invasive carcinoma. It is highly irregular and infiltrative."
            },
            "glioblastoma": {
                "steps": [
                    "Observation 1: Large ring-enhancing lesion in the left hemisphere crossing the corpus callosum.",
                    "Observation 2: Surrounding vasogenic edema causing mass effect.",
                    "Conclusion: Butterfly glioma, highly suggestive of Glioblastoma Multiforme (GBM)."
                ],
                "summary": "--- RADIOLOGIST FINDINGS SUMMARY ---\nComplex ring-enhancing lesion crossing the midline with significant necrotic center and surrounding edema. \n\nDifferential Diagnosis: Glioblastoma Multiforme (GBM), Primary CNS Lymphoma.",
                "image": "case2_brain_mri.png",
                "query_resp": "The lesion crossing the midline ('butterfly' pattern) with central necrosis is pathognomonic for Glioblastoma. Lymphoma is possible but typically shows homogeneous enhancement."
            },
            "breast_carcinoma": {
                "steps": [
                    "Observation 1: Clustered pleomorphic microcalcifications in the upper outer quadrant.",
                    "Observation 2: Associated architectural distortion and stromal thickening.",
                    "Conclusion: Suspicious for DCIS or invasive ductal carcinoma (BI-RADS 5)."
                ],
                "summary": "--- RADIOLOGIST FINDINGS SUMMARY ---\nSegmental distribution of fine linear and branching microcalcifications with adjacent architectural distortion. \n\nDifferential Diagnosis: Ductal Carcinoma in Situ (DCIS), Invasive Ductal Carcinoma.",
                "image": "case3_mammogram.png",
                "query_resp": "The microcalcifications show a fine, linear, and branching morphology, which is highly suspicious for comedo-type necrosis seen in high-grade DCIS."
            },
            "healthy_lung": {
                "steps": [
                    "Observation 1: Lung parenchyma is clear bilaterally.",
                    "Observation 2: No focal consolidations, masses, or pleural effusions.",
                    "Conclusion: Normal chest CT. No evidence of acute or chronic disease."
                ],
                "summary": "--- RADIOLOGIST FINDINGS SUMMARY ---\nUnremarkable CT of the chest. The tracheobronchial tree is patent. No suspicious pulmonary nodules or masses are identified. \n\nDifferential Diagnosis: Healthy Patient (True Negative).",
                "image": "outlier1_healthy_lung.png",
                "query_resp": "There are absolutely no ground-glass opacities or structural abnormalities. The patient's routine screening is clear."
            },
            "false_positive_lung": {
                "steps": [
                    "Observation 1: Well-circumscribed nodule in the left lower lobe with internal 'popcorn' calcifications.",
                    "Observation 2: Smooth margins, no aggressive features or spiculation.",
                    "Conclusion: Benign pulmonary hamartoma. No further action required."
                ],
                "summary": "--- RADIOLOGIST FINDINGS SUMMARY ---\nA 1.2 cm well-defined nodule with macroscopic fat and central popcorn calcification is noted in the LLL. This classical appearance is diagnostic of a benign hamartoma. \n\nDifferential Diagnosis: Pulmonary Hamartoma (Benign), Carcinoid tumor (less likely due to calcification pattern).",
                "image": "outlier2_false_positive_lung.png",
                "query_resp": "While it may trigger basic AI anomaly detection, the presence of macroscopic fat and 'popcorn' calcification confirms it as a completely benign hamartoma (False Positive for malignancy)."
            }
        }

    async def analyze_report_for_radiologist(self, report_content: str, metadata: dict):
        scenario_key = metadata.get("scenario_key", "healthy_lung")
        data = self.scenarios[scenario_key]
        
        yield f"Initializing Radiologist-grade analysis for scenario: {scenario_key}..."
        await asyncio.sleep(0.5)
        yield "Correlating imaging modalities with anomalies..."
        await asyncio.sleep(0.5)

        for step in data["steps"]:
            yield step
            await asyncio.sleep(0.5)

        await asyncio.sleep(0.5)
        yield json.dumps({"text": data["summary"], "image": data["image"]})

    async def stream_advanced_query(self, report_content: str, query: str, metadata: dict = None):
        scenario_key = metadata.get("scenario_key", "healthy_lung") if metadata else "healthy_lung"
        resp = self.scenarios[scenario_key]["query_resp"]
        
        words = resp.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.1)


async def run_complex_dry_run():
    print("==========================================================")
    print("--- ADVANCED RADIOLOGIST AI : COMPLEX DRY RUN SETTINGS ---")
    print("==========================================================\n")
    
    ai = MockRadiologistAI()
    
    scenarios = [
        {
            "id": "Case 1",
            "name": "Advanced Lung Cancer (CT)",
            "key": "lung_cancer",
            "query": "Is the margin of the opacity spiculated or smooth? What does it indicate?",
            "metadata": {"age": 68, "imaging_modality": "CT Scan", "clinical_notes": "Heavy smoker, recent hemoptysis.", "scenario_key": "lung_cancer"},
            "report": "Large irregular mass in right upper lobe with spiculated margins."
        },
        {
            "id": "Case 2",
            "name": "Brain Glioblastoma (MRI)",
            "key": "glioblastoma",
            "query": "Why do you suspect Glioblastoma over Primary CNS Lymphoma?",
            "metadata": {"age": 55, "imaging_modality": "MRI Brain", "clinical_notes": "Progressive headaches, left-sided weakness.", "scenario_key": "glioblastoma"},
            "report": "Large ring-enhancing lesion crossing the corpus callosum with extensive edema."
        },
        {
            "id": "Case 3",
            "name": "Breast Carcinoma (Mammogram)",
            "key": "breast_carcinoma",
            "query": "What specific morphology do the microcalcifications exhibit?",
            "metadata": {"age": 42, "imaging_modality": "Mammography", "clinical_notes": "Palpable lump in upper outer quadrant.", "scenario_key": "breast_carcinoma"},
            "report": "Pleomorphic microcalcifications in a segmental distribution with architectural distortion."
        },
        {
            "id": "Outlier 1",
            "name": "Healthy Lung (True Negative CT)",
            "key": "healthy_lung",
            "query": "Are there any subtle ground-glass opacities indicative of early infection?",
            "metadata": {"age": 30, "imaging_modality": "CT Scan", "clinical_notes": "Routine screening. Asymptomatic.", "scenario_key": "healthy_lung"},
            "report": "Clear lung fields bilaterally. No effusions or masses."
        },
        {
            "id": "Outlier 2",
            "name": "Pulmonary Hamartoma (False Positive CT)",
            "key": "false_positive_lung",
            "query": "Why should this nodule not be biopsied?",
            "metadata": {"age": 50, "imaging_modality": "CT Scan", "clinical_notes": "Incidental nodule finding on pre-op chest CT.", "scenario_key": "false_positive_lung"},
            "report": "Well-circumscribed nodule with popcorn calcification and fat density."
        }
    ]

    for sc in scenarios:
        print(f"[{sc['id']}] Processing: {sc['name']}")
        print(f"Patient Metadata: {json.dumps(sc['metadata'])}")
        print(f"Initial Report Context: {sc['report']}")
        print("-" * 50)
        
        print(">>> STREAMING AI ANALYSIS:")
        async for step in ai.analyze_report_for_radiologist(sc['report'], sc['metadata']):
            print(f"  > {step}")
            
        print("\n>>> RADIOLOGIST ADVANCED QUERY:")
        print(f"Query: '{sc['query']}'")
        print("Response: ", end="")
        async for chunk in ai.stream_advanced_query(sc['report'], sc['query'], sc['metadata']):
            print(chunk, end="", flush=True)
        print("\n")
        print("=" * 58 + "\n")
        
        await asyncio.sleep(1.0)
        
    print("--- COMPLEX DRY RUN COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_complex_dry_run())
