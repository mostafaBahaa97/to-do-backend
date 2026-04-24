from fastapi import FastAPI, Body ,Request
from supabase import create_client
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os


# إعدادات Supabase (تأكد من وضعها في Environment Variables على Railway)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في المستقبل ممكن تغير "*" لرابط فيرسيل بتاعك للأمان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoItem(BaseModel):
    task_text: str

@app.post("/add-todo")
async def add_todo(request: Request): 
    try:
        # قراءة البيانات الخام من الـ body
        payload = await request.json()
        text = payload.get("task_text")
        
        if not text:
            return {"status": "error", "message": "No task text provided"}

        priority = "Medium"
        if any(word in text.lower() for word in ["urgent", "ضروري", "حالا"]):
            priority = "High"
            
        data = supabase.table("todos").insert({
            "task": text,
            "priority": priority
        }).execute()
        
        return {"status": "success", "data": data.data}
    except Exception as e:
        print(f"Server Error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data