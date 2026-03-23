from crewai.tools import BaseTool
import os
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools.tools.qdrant_vector_search_tool.qdrant_search_tool import (
    QdrantVectorSearchTool,
    QdrantConfig,
)
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def groq_embedding(text: str) -> list[float]:
    """Generate embeddings using local sentence-transformers."""
    return embedding_model.encode(text).tolist()

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."


class FixedQdrantSchema(BaseModel):
    query: str = Field(..., description="Query to search in Qdrant DB - always required.")
    filter_by: str | None = Field(default=None, description="Parameter to filter the search by. When filtering, needs to be used in conjunction with filter_value.")
    filter_value: str | None = Field(default=None, description="Value to filter the search by. When filtering, needs to be used in conjunction with filter_by.")

class FixedQdrantTool(QdrantVectorSearchTool):
    args_schema: Type[BaseModel] = FixedQdrantSchema
def make_qdrant_tool():
    return FixedQdrantTool(
        qdrant_config=QdrantConfig(
            qdrant_url="http://localhost:6333",
            qdrant_api_key=None,
            collection_name="pdf_rag_collection",
            limit=3,
            score_threshold=0.35,
        ),
        custom_embedding_fn=groq_embedding
    )

# PDF loading function
import uuid
import pdfplumber
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

def load_pdf_to_qdrant(pdf_path: str, collection_name: str = "pdf_rag_collection"):
    # Initialize Qdrant client
    qdrant = QdrantClient(url="http://localhost:6333")
    
    # Extract text from PDF
    text_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text.strip())
    
    # Create collection if not exists
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
           vectors_config=VectorParams(size=384, distance=Distance.COSINE)   
            
            )
    
    # Store embeddings
    points = []
    for chunk in text_chunks:
        embedding = groq_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        ))
    qdrant.upsert(collection_name=collection_name, points=points)
    print(f"Loaded {len(points)} chunks into Qdrant.")

def load_text_to_qdrant(text_path: str, collection_name: str = "pdf_rag_collection"):
    # Initialize Qdrant client
    qdrant = QdrantClient(url="http://localhost:6333")
    
    # Read text from file
    with open(text_path, 'r') as f:
        text = f.read()
    
    # Split text into chunks (simple approach - split by paragraphs)
    text_chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
    
    # Create collection if not exists
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    
    # Store embeddings
    points = []
    for chunk in text_chunks:
        embedding = groq_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        ))
    qdrant.upsert(collection_name=collection_name, points=points)
    print(f"Loaded {len(points)} text chunks into Qdrant.")