from fastapi import FastAPI, Body
from supabase import create_client
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Annotated


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
        # 1. طباعة الطلب الخام للتأكد من وصوله
        body = await request.json()
        print(f"DEBUG: Received body: {body}") # هتظهر في Railway Logs
        
        task_text = body.get("task_text")
        
        if not task_text:
            return {"status": "error", "message": "Field 'task_text' is missing"}

        # 2. تنفيذ الإضافة في Supabase
        res = supabase.table("todos").insert({
            "task": task_text,
            "priority": "Medium"
        }).execute()
        
        return {"status": "success", "data": res.data}
    except Exception as e:
        print(f"DEBUG: Error occurred: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data
