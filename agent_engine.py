import asyncio
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class AgentEngine:
    def __init__(self):
        # Initialize Gemini Client if API key is present
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key and api_key != "your_api_key_here":
            self.client = genai.Client(api_key=api_key)
            self.model_name = "gemini-2.5-flash"
        else:
            self.client = None
            print("WARNING: GEMINI_API_KEY not set or invalid in .env")

    def _get_report_content(self, filename: str) -> str:
        """Helper to match filename mock with actual physical data log."""
        report_path = ""
        filename_lower = filename.lower()
        if "lung" in filename_lower:
            report_path = "data/lung_cancer_report.txt"
        elif "breast" in filename_lower:
            report_path = "data/breast_cancer_report.txt"
        elif "diab" in filename_lower:
            report_path = "data/diabetes_report.txt"
        elif "hered" in filename_lower:
            report_path = "data/hereditary_disease_report.txt"
        
        if report_path and os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                return f.read()
        return "No specific report text found. General patient data assumed."

    async def analyze_report(self, filename: str, content_size: int):
        yield f"Agent Initialized. Receiving report: {filename} ({content_size} bytes)"
        await asyncio.sleep(0.5)

        if not self.client:
            yield "WARNING: No Gemini API Key configured!! Please set GEMINI_API_KEY in .env"
            yield json.dumps({"text": "Error: Gemini API not configured.", "image": "none"})
            return

        yield "Parsing medical report format and initiating Gemini Advanced Analysis..."
        await asyncio.sleep(0.5)

        report_content = self._get_report_content(filename)

        prompt = f"""You are a top-tier medical AI agent acting as a diagnosis specialist processing {filename}.
Analyze the following patient report.

Report Content:
{report_content}

Provide your response strictly in the following JSON format without Markdown blocks (like ```json), just raw valid JSON:
{{
  "steps": ["Step 1 thought: <what you are extracting>", "Step 2 thought: <what you are correlating>", "Step 3 thought: <diagnostic conclusion>"],
  "final_diagnosis_summary": "--- FINAL DIAGNOSIS SUMMARY ---\\n<Detailed summary>\\n\\nRecommendation: <Doctor recommendation>",
  "image_reference_guess": "Pick closely matching graphic: lung_ct.png, breast_mri.png, brain_mri.png, or none"
}}
"""
        try:
            # Generate the content as a JSON block using Gemini
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            
            # Clean possible markdown wrapping from LLM output
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw_text)
            
            # Stream the steps progressively back to simulating the 'thinking' process
            for step in data.get("steps", []):
                yield step
                await asyncio.sleep(0.8)
                
            final_report = data.get("final_diagnosis_summary", "Diagnosis summary generation failed.")
            image_ref = data.get("image_reference_guess", "none")
            
            await asyncio.sleep(0.5)
            # Send the final structured payload expected by the frontend
            yield json.dumps({"text": final_report, "image": image_ref})
            
        except Exception as e:
            yield f"Error during Gemini analysis: {str(e)}"
            final_report = "--- FINAL DIAGNOSIS SUMMARY ---\nAnalysis failed due to an error."
            yield json.dumps({"text": final_report, "image": "none"})

    async def answer_query(self, filename: str, query: str):
        if not self.client:
             yield "Gemini API Key is not set. Cannot perform real-time reasoning."
             return
             
        report_content = self._get_report_content(filename)
        
        system_prompt = f"""You are a helpful, professional medical AI assistant.
Answer the user's query specifically related to their report context below. 
Be conversational, reassuring, but medically accurate. 

Report Context:
{report_content}

User Query: {query}
"""
        try:
            # Stream the answer live chunk-by-chunk over the websocket
            response = await self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=system_prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            async for chunk in response:
                # Yield text and introduce strict minimal sleep sequence for the UI to consume smoothly if needed
                yield chunk.text
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"Error querying Gemini: {str(e)}"
