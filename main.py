from fastapi import FastAPI, Body
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
async def add_todo(item: TodoItem):
    print(f"Received request with item: {item}")
    print(f"Task text: {item.task_text}")
    
    try:
        text = item.task_text
        
        if not text:
            return {"status": "error", "message": "No task text provided"}

        priority = "Medium"
        if any(word in text.lower() for word in ["urgent", "ضروري", "حالا"]):
            priority = "High"
            
        data = supabase.table("todos").insert({
            "task": text,
            "priority": priority
        }).execute()
        
        print(f"Data inserted successfully: {data.data}")
        return {"status": "success", "data": data.data}
    except Exception as e:
        print(f"Server Error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data
