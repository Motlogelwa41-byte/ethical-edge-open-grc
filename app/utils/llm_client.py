import os
import json
import asyncio
from typing import Dict, Any
import httpx
from fastapi import HTTPException, status

# The runtime environment injects this key. We declare it as an empty string fallback.
GEMINI_API_KEY = ""

class AIAuditorClient:
    def __init__(self):
        """
        Initializes the audit engine with the required Gemini 2.5 model endpoints.
        """
        # Resolve the active API key through the runtime variable or local environment
        self.api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.model_name = "gemini-2.5-flash-preview-09-2025"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

    def _load_prompt_template(self) -> str:
        """
        Loads the system-level audit instructions from the repository.
        """
        prompt_path = "ai_auditor_prompt.txt"
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Required system audit guidelines missing at: {prompt_path}")
            
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    async def execute_document_audit(self, gate_id: str, requirement_text: str, document_text: str) -> Dict[str, Any]:
        """
        Sends the audit parameters to the Gemini API utilizing structured JSON outputs
        and a strict 5-tier exponential backoff retry loop.
        """
        system_prompt = self._load_prompt_template()
        user_payload = f"TARGET_GATE_ID: {gate_id}\nREQUIREMENT_TEXT: {requirement_text}\nRAW_EVALUATION_DOCUMENT:\n{document_text}"

        # Build the exact API payload format required by Gemini 2.5
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": user_payload}
                    ]
                }
            ],
            "systemInstruction": {
                "parts": [
                    {"text": system_prompt}
                ]
            },
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "gate_id": {"type": "STRING"},
                        "is_passed": {"type": "BOOLEAN"},
                        "confidence_score": {"type": "NUMBER"},
                        "evidence_citation": {"type": "STRING"},
                        "risk_rating": {
                            "type": "STRING", 
                            "enum": ["LOW", "MEDIUM", "HIGH"]
                        }
                    },
                    "required": ["gate_id", "is_passed", "confidence_score", "evidence_citation", "risk_rating"]
                }
            }
        }

        # Mandatory Exponential Backoff Delays (1s, 2s, 4s, 8s, 16s)
        backoff_delays = [1, 2, 4, 8, 16]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for attempt, delay in enumerate(backoff_delays):
                try:
                    response = await client.post(self.api_url, json=payload)
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        # Extract non-streaming text content from candidates list
                        raw_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(raw_text)
                    
                    # Raise for non-200 responses to trigger retry logic
                    response.raise_for_status()

                except Exception:
                    # If this was our final retry, fail gracefully with a user-friendly message
                    if attempt == len(backoff_delays) - 1:
                        raise HTTPException(
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="The automated compliance evaluation node is currently experiencing high demand. Please try uploading your document again shortly."
                        )
                    # Pause execution silently without logging system details to the console
                    await asyncio.sleep(delay)
                    
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected verification fault occurred on the auditing subsystem interface."
