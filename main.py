from fastapi import FastAPI
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
async def add_todo(item: TodoItem): # استلام البيانات كـ JSON Body
    try:
        priority = "Medium"
        if any(word in item.task_text.lower() for word in ["urgent", "ضروري", "حالا"]):
            priority = "High"
            
        data = supabase.table("todos").insert({
            "task": item.task_text,
            "priority": priority
        }).execute()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data