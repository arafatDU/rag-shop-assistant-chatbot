from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.init_db import create_tables
from routes import chat, products
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    print("✅ Database tables created successfully!")
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Shop Assistant RAG Chatbot API", 
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(products.router)

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Shop Assistant RAG Chatbot API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "postgresql"}

def main():
    print("🚀 Starting Shop Assistant RAG Chatbot API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()