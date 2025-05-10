import cohere
import requests
from PyPDF2 import PdfReader
from io import BytesIO

# Cohere client
co = cohere.Client("vzSUUNFPnI6IBHil4qwn0rQxVDegkZaHL9cZNNiR")

def extract_text_from_pdf(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200 or not response.content:
        print(f"Failed to download PDF from {url}")
        return ""
    
    try:
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages[:5]:  # Limit pages for speed
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        print(f"Error reading PDF from {url}: {e}")
        return ""

pdf_urls = [
    "https://www.poshantracker.in/pdf/Awareness/MilletsRecipeBook2023_Low%20Res_V5.pdf",
    "https://www.cardiff.ac.uk/__data/assets/pdf_file/0003/123681/Recipe-Book.pdf"
]

combined_text = "\n\n".join([extract_text_from_pdf(url) for url in pdf_urls])

ingredients = "potatoes, tomatoes, onions, garlic, ginger, chicken"
prompt = f"""
You are a recipe assistant. Based on the ingredients: {ingredients}, suggest a quick dinner recipe.
Use the following recipe content for reference:
{combined_text[:3000]}
"""

response = co.chat(message=prompt, model="command-r-plus")
print(response.text)
