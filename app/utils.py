import re
import requests
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    # Remove script and style elements first
    soup = BeautifulSoup(text, "html.parser")
    for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
        script_or_style.decompose()
        
    text = soup.get_text(separator=" ")
    
    # Standard cleaning
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9., ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def load_page(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text