from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="Simple REST API", version="1.0.0")

# Initialize dictionary with sample data
data_store: Dict[str, Any] = {
    "user1": {"name": "Alice", "age": 25, "city": "New York"},
    "user2": {"name": "Bob", "age": 30, "city": "San Francisco"},
    "user3": {"name": "Charlie", "age": 35, "city": "London"},
    "product1": {"name": "Laptop", "price": 999.99, "stock": 10},
    "product2": {"name": "Phone", "price": 699.99, "stock": 25},
    "config": {"theme": "dark", "language": "en", "notifications": True}
}

# Pydantic model for POST requests
class UpdateData(BaseModel):
    value: Any


def build_response(content: dict, cache: bool = False) -> JSONResponse:
    """
    Utility function to build JSON responses with custom headers.
    """
    headers = {
        "Content-Type": "application/json",
        "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }
    if cache:
        headers["Cache-Control"] = "public, max-age=60"  # cache for 60 seconds

    return JSONResponse(content=content, headers=headers)


@app.get("/")
async def root():
    return build_response({
        "message": "Simple REST API Server",
        "endpoints": {
            "GET": "/data/{key} - Get value by key",
            "POST": "/data/{key} - Update value by key",
            "GET": "/data - Get all data"
        }
    })


@app.get("/data/{key}")
async def get_data(key: str):
    if key not in data_store:
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found")

    return build_response({
        "key": key,
        "value": data_store[key],
        "status": "success"
    }, cache=True)


@app.get("/data")
async def get_all_data():
    return build_response({
        "data": data_store,
        "count": len(data_store),
        "status": "success"
    })


@app.post("/data/{key}")
async def update_data(key: str, update: UpdateData):

    data_store[key] = update.value

    return build_response({
        "key": key,
        "new_value": update.value,
        "status": "success"
    })


@app.get("/health")
async def health_check():
    return build_response({
        "status": "healthy",
        "data_count": len(data_store)
    })


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )