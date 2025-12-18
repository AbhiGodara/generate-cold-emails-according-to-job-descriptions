import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts import JOB_EXTRACTION_PROMPT

load_dotenv()

class JobExtractor:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def extract(self, text: str):
        response = self.llm.invoke(
            JOB_EXTRACTION_PROMPT.format(page_data=text)
        )

        raw = response.content.strip()

        # Improved JSON extraction using Regex to find the array [ ... ]
        # This handles cases where the LLM wraps code in ```json ... ```
        match = re.search(r'\[\s*{.*}\s*\]', raw, re.DOTALL)
        
        if not match:
            print(f"DEBUG: LLM Raw Output -> {raw}")
            raise ValueError("The AI could not find a valid job list on this page.")

        try:
            jobs = json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse job data: {e}")

        if not isinstance(jobs, list):
            return []

        cleaned = []
        for job in jobs:
            if isinstance(job, dict):
                cleaned.append({
                    "role": job.get("role", "Unknown Role"),
                    "experience": job.get("experience", "Not specified"),
                    "skills": job.get("skills", []) if isinstance(job.get("skills"), list) else [],
                    "description": job.get("description", "")
                })

        return cleaned