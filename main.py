from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from agent_engine import AgentEngine
from hospital_integration_api import router as radiology_router

app = FastAPI(title="Therapeutic Agent API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(radiology_router)

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    await websocket.accept()
    engine = AgentEngine()
    try:
        # Wait for client to send start signal with file metadata
        data = await websocket.receive_json()
        filename = data.get("filename", "unknown_report.pdf")
        size = data.get("size", 0)
        
        # Stream the agent's analysis back to the client
        async for step in engine.analyze_report(filename, size):
            await websocket.send_json({"type": "step", "content": step})
            
        await websocket.send_json({"type": "analysis_complete"})

        # Listen for advanced queries
        while True:
            query_data = await websocket.receive_json()
            if query_data.get("type") == "query":
                query_text = query_data.get("text", "")
                await websocket.send_json({"type": "query_ack"})
                
                # Stream the agent's query response
                async for chunk in engine.answer_query(filename, query_text):
                    await websocket.send_json({"type": "query_response_chunk", "content": chunk})
                
                await websocket.send_json({"type": "query_response_complete"})

    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
