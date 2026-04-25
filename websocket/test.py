import asyncio
import websockets
import json


async def simple_stream():
    uri = "ws://localhost:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        try:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                print("Data: ", data)

                if data.get("type") in ("complete", "error"):
                    break
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")


if __name__ == "__main__":
    asyncio.run(simple_stream())
