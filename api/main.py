from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum  # 讓 FastAPI 運作於 Serverless

app = FastAPI()

# 允許跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 用 dictionary 儲存資料 (demo用)
data = {
    "likes": 0,
    "comments": [],
    "commentCount": 0
}

# 取得貼文資料
@app.get("/post")
def get_post():
    return data

# 按讚
@app.post("/like")
def add_like():
    data["likes"] += 1
    return data

# 留言資料模型
class Comment(BaseModel):
    text: str

# 新增留言
@app.post("/comment")
def add_comment(comment: Comment):
    data["comments"].append(comment.text)
    data["commentCount"] = len(data["comments"])
    return data

# Vercel Serverless handler
handler = Mangum(app)
