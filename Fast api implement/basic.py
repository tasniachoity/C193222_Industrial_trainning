from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Optional, List, Dict

app = FastAPI()

news = {
    1: {
        "id": 1,
        "title": "Top 10 programming language",
        "content": "Python is the most popular programming language",
        "author": "Kalim"
    },
    2: {
        "id": 2,
        "title": "LLM race in modern era",
        "content": "Content on modern LLM models",
        "author": "Raisa"
    },
    3: {
        "id": 3,
        "title": "Latest LLM model from Mistral!!!",
        "content": "Content on modern LLM models both close & open source",
        "author": "Kalim"
    },
    4: {
        "id": 4,
        "title": "What's the Google calls on LLM!!!",
        "content": "Content on modern LLM models both close & open source",
        "author": "Sazzad"
    }
}

# Pydantic model for creating and updating news articles
class News(BaseModel):
    title: str
    content: Optional[str] = None
    author: str

class UpdateNews(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None

@app.get("/news", response_model=Dict[int, News])
def get_news():
    return news

@app.get("/news/author/{author}", response_model=List[Dict])
def get_news_by_author(author: str, title_contains: Optional[str] = None):
    filtered_news = [article for article in news.values() if article["author"].lower() == author.lower()]
    
    if title_contains:
        filtered_news = [article for article in filtered_news if title_contains.lower() in article["title"].lower()]
    
    if not filtered_news:
        raise HTTPException(status_code=404, detail="No news articles found for this author with the specified title filter.")
    
    return filtered_news

@app.post("/create_news", response_model=Dict)
def create_news(input_news: News):
    new_id = max(news.keys()) + 1
    news[new_id] = {
        "id": new_id,
        "title": input_news.title,
        "content": input_news.content,
        "author": input_news.author
    }
    return news[new_id]

@app.put("/update_news/{id}", response_model=Dict)
def update_news(id: int, input: UpdateNews):
    if id not in news:
        raise HTTPException(status_code=404, detail=f"News item with ID {id} not found.")
    
    if input.title is not None:
        news[id]["title"] = input.title
    if input.content is not None:
        news[id]["content"] = input.content
    if input.author is not None:
        news[id]["author"] = input.author
    
    return news[id]

@app.delete("/delete_news/{id}", response_model=Dict)
def delete_news(id: int):
    if id not in news:
        raise HTTPException(status_code=404, detail=f"News item with ID {id} not found.")
    
    del news[id]
    return {"message": "News Deleted Successfully"}

if __name__ == '__main__':
    uvicorn.run("expanded:app", host='127.0.0.1', port=8000, reload=True)
