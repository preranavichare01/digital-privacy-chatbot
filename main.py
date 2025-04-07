from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load .env
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.post("/ask", response_class=HTMLResponse)
async def ask_ai(request: Request, prompt: str = Form(...)):
    try:
        chat_completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers only questions about digital privacy, digital laws, cybersecurity, and data protection."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = chat_completion.choices[0].message.content
    except Exception as e:
        answer = f"Error: {str(e)}"

    return templates.TemplateResponse("privacy.html", {
        "request": request,
        "response": {"answer": answer},
        "prompt": prompt
    })
