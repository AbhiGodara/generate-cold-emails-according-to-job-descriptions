import random
import os
from langchain_groq import ChatGroq
from prompts import (
    SKILLS_FIRST_PROMPT,
    VALUE_FIRST_PROMPT,
    CULTURE_FIRST_PROMPT
)



class EmailGenerator:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.strategies = {
            "skills": SKILLS_FIRST_PROMPT,
            "value": VALUE_FIRST_PROMPT,
            "culture": CULTURE_FIRST_PROMPT
        }

    def generate(self, job):
        strategy = random.choice(list(self.strategies.keys()))
        prompt = self.strategies[strategy]

        links = self.portfolio.query(job["skills"])

        if not isinstance(links, list):
            links = []

        links = [str(l) for l in links]

        filled_prompt = prompt.format(
            role=job["role"],
            experience=job["experience"],
            skills=", ".join(job["skills"]),
            links=", ".join(links)
        )

        # 🔥 THIS IS THE MISSING STEP
        response = self.llm.invoke(filled_prompt)

        email = response.content.strip()

        explanation = self._explain(strategy, job)

        return email, explanation

    def _explain(self, strategy, job):
        points = [
            f"Used **{strategy}-first** email strategy",
            f"Aligned messaging with the **{job['role']}** role",
        ]

        if job["skills"]:
            points.append(f"Emphasized role-relevant skills: {', '.join(job['skills'][:3])}")

        if job.get("experience") != "Not specified":
            points.append(f"Adjusted tone for experience level: {job['experience']}")

        points.append("Kept structure concise and recruiter-friendly")

        return "\n".join(f"- {p}" for p in points)

