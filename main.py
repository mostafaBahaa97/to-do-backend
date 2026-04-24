from fastapi import FastAPI, Request
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
class TodoItem(BaseModel):
    task_text: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في المستقبل ممكن تغير "*" لرابط فيرسيل بتاعك للأمان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data


@app.post("/add-todo")
async def add_todo(task_text: str = None, request: Request = None):
    try:
        # لو مبعوتة كـ Query Param في اللينك
        final_text = task_text
        
        # لو مبعوتة كـ JSON Body
        if not final_text and request:
            body = await request.json()
            final_text = body.get("task_text")

        if not final_text:
            return {"status": "error", "message": "No task text provided"}

        res = supabase.table("todos").insert({"task": final_text}).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

