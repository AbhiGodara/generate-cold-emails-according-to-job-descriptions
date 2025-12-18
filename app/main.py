import sys
import streamlit as st

from extractor import JobExtractor
from email_generator import EmailGenerator
from portfolio import Portfolio
from utils import clean_text, load_page

st.set_page_config(
    layout="wide",
    page_title="Cold Email Generator",
    page_icon="📧"
)

def run_app():
    st.title("📧 Cold Email Generator (GenAI System)")

    url = st.text_input(
        "Enter a job posting URL",
        value="https://jobs.nike.com/job/R-33460"
    )

    if st.button("Generate Emails"):
        try:
            raw_text = load_page(url)
            cleaned_text = clean_text(raw_text)
            cleaned_text=cleaned_text[:20000]  # Limit to first 20k chars

            # 🚨 Dynamic / unsupported page detection
            if len(cleaned_text) < 500:
                st.error(
                    "⚠️ Unable to extract sufficient job information.\n\n"
                    "This page likely loads content dynamically using JavaScript.\n"
                    "Please provide a static job posting URL (company careers page)."
                )
                st.stop()

            extractor = JobExtractor()
            jobs = extractor.extract(cleaned_text)
            st.write("DEBUG: jobs extracted →", jobs)

            if not jobs:
                st.error(
                    "❌ No job roles could be extracted from this page.\n\n"
                    "This usually means the page content is not structured like a job description."
                )
                st.stop()

            portfolio = Portfolio()
            portfolio.load()

            generator = EmailGenerator(portfolio)

            for idx, job in enumerate(jobs, start=1):
                st.markdown(f"## 🧩 Role {idx}: {job['role']}")
                email, explanation = generator.generate(job)

                st.code(email, language="markdown")

                with st.expander("Why this email?"):
                    st.write(explanation)

        except Exception as e:
            st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    run_app()
