from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import os
import asyncio
from radiology_plugin import RadiologistAI

router = APIRouter(prefix="/api/radiology", tags=["Hospital Integration"])

# We define a helper to mock pulling records out of an EMR (like Aditya Birla MVP EMR system would)
def mock_fetch_emr_data(patient_id: str) -> str:
    # Fallback to local files for MVP testing
    report_path = ""
    patient_id_lower = patient_id.lower()
    if "lung" in patient_id_lower:
        report_path = "data/lung_cancer_report.txt"
    elif "breast" in patient_id_lower:
        report_path = "data/breast_cancer_report.txt"
    elif "diab" in patient_id_lower:
        report_path = "data/diabetes_report.txt"
    elif "hered" in patient_id_lower:
        report_path = "data/hereditary_disease_report.txt"
        
    if report_path and os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            return f.read()
    return "No clinical data found for this patient ID. Missing EMR Record."

@router.websocket("/ws/radiologist_assist")
async def radiologist_websocket(websocket: WebSocket):
    """
    Plug-and-play WebSocket endpoint for hospital applications to dial into
    advanced real-time AI assistance for Radiologists using Mistral.
    """
    await websocket.accept()
    ai_assistant = RadiologistAI()
    
    patient_id = "unknown"
    report_content = "No context"

    try:
        # Phase 1: Wait for initialization payload from hospital dashboard
        init_data = await websocket.receive_json()
        patient_id = init_data.get("patient_id", "anon")
        metadata = init_data.get("metadata", {})
        
        # Load EMR report for this session
        report_content = mock_fetch_emr_data(patient_id)

        # Stream structural analysis first
        async for step in ai_assistant.analyze_report_for_radiologist(report_content, metadata):
            await websocket.send_json({"type": "step", "content": step})
            
        await websocket.send_json({"type": "analysis_complete"})

        # Phase 2: Live Advanced Question Handling Loop
        while True:
            query_data = await websocket.receive_json()
            if query_data.get("type") == "query":
                query_text = query_data.get("text", "")
                await websocket.send_json({"type": "query_ack"})
                
                # Stream the Mistral advanced query answers back
                async for chunk in ai_assistant.stream_advanced_query(report_content, query_text):
                    await websocket.send_json({"type": "query_response_chunk", "content": chunk})
                
                await websocket.send_json({"type": "query_response_complete"})

    except WebSocketDisconnect:
        print(f"Radiologist Disconnected from session for patient: {patient_id}")
