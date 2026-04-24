from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# مهم جداً للسماح للفرونت اند (Vercel) بالاتصال بالباك اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # في الإنتاج ضع رابط موقعك على فيرسيل هنا
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Todo API"}
