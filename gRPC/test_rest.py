import requests
import time

url = "http://localhost:8000/embed"
data = {"text": "Hello, I am testing REST embeddings!"}

start = time.time()
response = requests.post(url, json=data)
end = time.time()

print("⏱️ Total request time:", end - start, "seconds")