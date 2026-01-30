import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import neighborhoods, feedback

app = FastAPI(
    title="Sound City API",
    description="API for Münster neighborhood livability data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

allow_origins = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:5173,
    "https://web-production-1b810.up.railway.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(feedback.router)
app.include_router(neighborhoods.router)

@app.get("/")
def root():
    """Root endpoint - API status check"""
    return {
        "message": "Welcome to Sound City API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "soundcity-api"}
