import os
import json
import asyncio
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

class RadiologistAI:
    def __init__(self):
        # Initialize Mistral Client if API key is present
        api_key = os.environ.get("MISTRAL_API_KEY")
        if api_key and api_key != "your_mistral_api_key_here":
            self.client = Mistral(api_key=api_key)
            self.model_name = "mistral-large-latest" # Using default robust model for medical domain
        else:
            self.client = None
            print("WARNING: MISTRAL_API_KEY not set or invalid in .env")

    async def analyze_report_for_radiologist(self, report_content: str, metadata: dict):
        """
        Analyze a raw imaging report and provide differential diagnosis and 
        correlations for a radiologist's review.
        """
        if not self.client:
             yield json.dumps({
                 "steps": ["Error: API Key missing"],
                 "final_diagnosis_summary": "Error: Mistral API not configured in the Hospital System integration.",
                 "image_reference_guess": "none"
             })
             return

        system_message = {
            "role": "system",
            "content": "You are an expert AI Radiologist Assistant. Process the raw radiological text and provide structured JSON focusing on differential diagnosis, anomalies, and clinical correlations designed for a senior radiologist."
        }
        
        user_message = {
            "role": "user",
            "content": f"""
Please analyze the following patient imaging report data.

Metadata context:
{json.dumps(metadata)}

Report Content:
{report_content}

Provide your response strictly in the following JSON format without Markdown blocks (like ```json), just raw valid JSON:
{{
  "steps": ["Observation 1: <anomaly detected>", "Observation 2: <correlation>", "Conclusion: <differential>"],
  "final_diagnosis_summary": "--- RADIOLOGIST FINDINGS SUMMARY ---\\n<Detailed medical summary>\\n\\nDifferential Diagnosis: <List>",
  "image_reference_guess": "Pick closely matching graphic: lung_ct.png, breast_mri.png, or none based on modality"
}}
"""
        }

        try:
            # We can mock steps for streaming the thought process since Mistral chat completion gives the final output
            yield "Initializing Radiologist-grade analysis via Mistral..."
            await asyncio.sleep(0.5)
            yield "Correlating imaging modalities with anomalies..."
            await asyncio.sleep(0.5)

            # Await the mistral API non-streaming chat for JSON block response
            res = await asyncio.to_thread(
                  self.client.chat.complete,
                  model=self.model_name,
                  messages=[system_message, user_message],
                  temperature=0.2
            )
            raw_text = res.choices[0].message.content
            # Clean markdown wrapping normally returned by LLMs
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw_text)

            # Stream steps from JSON back
            for step in data.get("steps", []):
                yield step
                await asyncio.sleep(0.8)

            final_report = data.get("final_diagnosis_summary", "Summary failed.")
            image_ref = data.get("image_reference_guess", "none")

            await asyncio.sleep(0.5)
            yield json.dumps({"text": final_report, "image": image_ref})

        except Exception as e:
            yield f"Error during Mistral analysis: {str(e)}"
            yield json.dumps({"text": f"--- RADIOLOGIST FINDINGS SUMMARY ---\nAnalysis failed due to an error: {str(e)}", "image": "none"})

    async def stream_advanced_query(self, report_content: str, query: str):
        """
        Streams response to an advanced specific radiologist query natively
        """
        if not self.client:
             yield "Mistral API Key is not set. Cannot perform real-time reasoning."
             return

        system_message = {
             "role": "system",
             "content": f"""You are a specialized Medical AI consulting with a senior radiologist. 
Answer advanced differential diagnosis questions based on this underlying context:

Report Context:
{report_content}
"""
        }
        
        user_message = {
            "role": "user",
            "content": f"Radiologist Query: {query}"
        }

        try:
             # Streaming the mistral response async
             response_stream = await self.client.chat.stream_async(
                 model=self.model_name,
                 messages=[system_message, user_message],
                 temperature=0.3
             )
             async for chunk in response_stream:
                 # mistralai v2 streaming format
                 if chunk.data.choices and len(chunk.data.choices) > 0 and chunk.data.choices[0].delta.content:
                     yield chunk.data.choices[0].delta.content
                     await asyncio.sleep(0.01)
        except Exception as e:
             yield f"\n[Error querying Mistral: {str(e)}]"
