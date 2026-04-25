from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import uvicorn
import json
from datetime import datetime

app = FastAPI(title="WebSocket Stream API", version="1.0.0")

# Sample words to stream
WORDS_LIST = [
    "Hello", "World", "FastAPI", "WebSocket", "Streaming", 
    "Python", "Async", "Real-time", "Data", "Complete"
]

@app.get("/")
async def root():
    return {
        "message": "WebSocket Stream Server",
        "websocket_url": "ws://localhost:8000/ws/stream",
        "info": "Connect to WebSocket to receive streaming words"
    }

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"Client connected: {websocket.client}")
    
    try:
        # Send initial message
        await websocket.send_text(json.dumps({
            "type": "info",
            "message": "Connected! Starting word stream...",
            "timestamp": datetime.now().isoformat()
        }))
        
        # Wait a moment before starting
        await asyncio.sleep(1)
        
        # Stream 10 words with 1-second gaps
        for i, word in enumerate(WORDS_LIST):
            message = {
                "type": "data",
                "word": word,
                "index": i + 1,
                "total": len(WORDS_LIST),
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send_text(json.dumps(message))
            print(f"Sent: {word} ({i+1}/{len(WORDS_LIST)})")
            
            # Wait 1 second before next word (except for last word)
            if i < len(WORDS_LIST) - 1:
                await asyncio.sleep(1)
        
        # Send completion message
        await websocket.send_text(json.dumps({
          "type": "complete",
            "message": "Stream complete!",
              "total_words": len(WORDS_LIST),
            "timestamp": datetime.now().isoformat()
        }))
        
        
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()





if __name__ == "__main__":
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )