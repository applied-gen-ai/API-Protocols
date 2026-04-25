# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
import uvicorn
import time

# Load embeddings model once
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    raise RuntimeError(f"Failed to load embeddings model: {e}")

app = FastAPI()

class EmbeddingRequest(BaseModel):
    text: str

@app.post("/embed")
async def get_embedding(req: EmbeddingRequest):
    try:
        start_time = time.time()
        vector = embeddings.embed_query(req.text)
        end_time = time.time()

        return {
            "embedding": list(vector),  # ensure JSON serializable
            "length": len(vector),
            "time_taken_sec": end_time - start_time,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {e}")

if __name__ == "__main__":
    uvicorn.run("rest:app", host="0.0.0.0", port=8000, reload=True)
