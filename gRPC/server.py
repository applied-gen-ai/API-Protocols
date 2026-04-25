##python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. embedding.proto


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import grpc
from concurrent import futures

import embedding_pb2_grpc
import embedding_pb2

from langchain_huggingface import HuggingFaceEmbeddings



# Load your embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Fixed class name: EmbeddingServiceServicer (not EmbeddingsServiceServicer)
#A base server class (EmbeddingServiceServicer)
class EmbeddingServiceServicer(embedding_pb2_grpc.EmbeddingServiceServicer):
    def GetEmbedding(self, request, context):
        try:
            # request.text contains the input text
            vector = embeddings.embed_query(request.text)
            
            # Fixed field name: embedding (not vector)
            return embedding_pb2.EmbeddingResponse(embedding=vector)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating embedding: {str(e)}")
            return embedding_pb2.EmbeddingResponse()


#Creates a thread pool gRPC server.
#Registers your service implementation and listens on port 50051
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Fixed class name here too
    embedding_pb2_grpc.add_EmbeddingServiceServicer_to_server(
        EmbeddingServiceServicer(), server
    )
    #A function to register your implementation (add_EmbeddingServiceServicer_to_server) with the gRPC server object.
    
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on port 50051")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server shutting down...")
        server.stop(0)


if __name__ == "__main__":
    serve()