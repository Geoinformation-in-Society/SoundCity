from fastapi import FastAPI
from app.routers import neighborhoods, feedback

app = FastAPI(
    title="Sound City API",
    description="API for Münster neighborhood livability data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
