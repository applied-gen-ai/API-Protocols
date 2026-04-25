import grpc
import time
import embedding_pb2
import embedding_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")  #opens a communication link (network channel) to your gRPC server.

stub = embedding_pb2_grpc.EmbeddingServiceStub(channel)  #lets you call the server’s methods as if they were local Python functions.

text = "Hello, I am testing gRPC embeddings!"

start = time.time()  # Start timer
response = stub.GetEmbedding(embedding_pb2.EmbeddingRequest(text=text))
end = time.time()  # End timer

print("Got embedding of length:", len(response.embedding)) 
print(f"Time taken: {end - start:.4f} seconds")


#A client stub (EmbeddingServiceStub).