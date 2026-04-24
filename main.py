from fastapi import FastAPI
from supabase import create_client
import os
from fastapi.middleware.cors import CORSMiddleware


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

@app.post("/add-todo")
async def add_todo(task_text: str):
    # فكرة "ذكية" بسيطة: تصنيف المهمة بناءً على كلمات مفتاحية
    priority = "Medium"
    if any(word in task_text.lower() for word in ["ضروري", "urgent", "deadline", "حالا"]):
        priority = "High"
    
    # إدخال البيانات في Supabase
    data, count = supabase.table("todos").insert({
        "task": task_text,
        "priority": priority
    }).execute()
    
    return {"status": "success", "data": data}

@app.get("/get-todos")
async def get_todos():
    response = supabase.table("todos").select("*").order("created_at", desc=True).execute()
    return response.data