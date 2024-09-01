from fastapi import FastAPI
import uvicorn

from app.routers import news, summary

# app = FastAPI()

app = FastAPI(
    title="AI based News Summary API",
    version="0.2",
    description="This is the API documentation for News Summary generating by AI.",
    
    contact={
        "name": "Team-1: Raisa Ahmed, Tasnia Fahrin, Efter Jahan",
        
    },
    redoc_url="/documentation",
    docs_url="/endpoints",
)

app.include_router(news.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summary API"}

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="localhost", port=8011, reload=True)