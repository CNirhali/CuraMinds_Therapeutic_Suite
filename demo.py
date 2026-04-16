import asyncio
import json
from radiology_plugin import RadiologistAI

async def run_demo():
    print("--- ADITYA BIRLA HOSPITAL : EMR INTEGRATION DEMO ---")
    print("Initializing Radiologist AI plug-and-play module...")
    
    # Initialize the core AI
    ai = RadiologistAI()
    
    # Mocking standard hospital patient retrieval step
    print("\n[Hospital UI] -> Requesting AI Diagnosis for Patient ID: 'lung_patient_A42'")
    metadata = {
        "age": 62,
        "imaging_modality": "CT Scan",
        "clinical_notes": "Chronic cough, suspected mass."
    }
    
    # Simulating the EMR data lookup that our websocket wrapper does
    report_content = "Patient history of smoking. Irregular opacity noted in upper right lobe. Further radiology analysis advised."
    
    print("\n--- AI STREAMING RESPONSE ---")
    
    # Stream the diagnosis
    async for step in ai.analyze_report_for_radiologist(report_content, metadata):
        print(f"  > {step}")
        await asyncio.sleep(0.5)
        
    print("\n[Hospital UI] -> Submitting specialized real-time question: 'Is the margin of the opacity spiculated or smooth?'")
    print("--- AI REALTIME CHAT RESPONSE ---")
    
    # Stream a live advanced query
    async for chunk in ai.stream_advanced_query(report_content, "Is the margin of the opacity spiculated or smooth?"):
        print(chunk, end="", flush=True)
    print("\n")
    print("--- DEMO COMPLETE ---")
    print("Note: If MISTRAL_API_KEY is not set, the AI will gracefully fallback to an error message.")

if __name__ == "__main__":
    asyncio.run(run_demo())
