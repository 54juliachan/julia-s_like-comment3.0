from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum  # 讓 FastAPI 可以 Serverless

app = FastAPI()

# 允許跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 用字典存資料 (刷新會重置)
data = {
    "likes": 0,
    "comments": [],
    "commentCount": 0
}

# 取得貼文資料
@app.get("/api/post")
def get_post():
    return data

# 按讚
@app.post("/api/like")
def add_like():
    data["likes"] += 1
    return data

# 留言模型
class Comment(BaseModel):
    text: str

# 新增留言
@app.post("/api/comment")
def add_comment(comment: Comment):
    data["comments"].append(comment.text)
    data["commentCount"] = len(data["comments"])
    return data

# Serverless handler
handler = Mangum(app)
