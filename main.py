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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في المستقبل ممكن تغير "*" لرابط فيرسيل بتاعك للأمان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoItem(BaseModel):
    task_text: str

# تغيير المسار لـ /create-task بدلاً من /add-todo
@app.post("/create-task") 
async def create_task(request: Request):
    try:
        body = await request.json()
        # طباعة واضحة جداً في اللوجز
        print(f"********** NEW CODE WORKING: {body} **********")
        
        task_text = body.get("task_text")
        if not task_text:
            return {"status": "error", "message": "No text"}

        res = supabase.table("todos").insert({"task": task_text}).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"status": "error", "message": str(e)}
    

@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data
