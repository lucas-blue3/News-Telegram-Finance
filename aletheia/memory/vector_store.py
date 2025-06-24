"""
Vector store implementation for long-term memory.
"""

import os
from typing import Dict, List, Optional, Any, Union

import chromadb
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.documents import Document


class VectorMemory:
    """
    Vector store implementation for long-term memory using ChromaDB.
    """
    
    def __init__(
        self,
        collection_name: str = "aletheia_memory",
        persist_directory: Optional[str] = None,
        embedding_function: Optional[Any] = None
    ):
        """
        Initialize the vector memory.
        
        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist the vector store
            embedding_function: Function to use for embeddings
        """
        # Set default persist directory if not provided
        if persist_directory is None:
            persist_directory = os.getenv("VECTOR_DB_PATH", "./data/vectordb")
        
        # Create the directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Set default embedding function if not provided
        if embedding_function is None:
            embedding_function = OpenAIEmbeddings(
                model="text-embedding-ada-002",
                base_url="https://api.deepseek.com/v1",  # Replace with actual DeepSeek API URL
            )
        
        # Initialize the vector store
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=persist_directory
        )
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add texts to the vector store.
        
        Args:
            texts: List of texts to add
            metadatas: List of metadata for each text
            ids: List of IDs for each text
            
        Returns:
            List of IDs of the added texts
        """
        return self.vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
            
        Returns:
            List of IDs of the added documents
        """
        return self.vectorstore.add_documents(documents=documents)
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search for similar documents in the vector store.
        
        Args:
            query: Query string
            k: Number of results to return
            filter: Filter to apply to the search
            
        Returns:
            List of similar documents
        """
        return self.vectorstore.similarity_search(query=query, k=k, filter=filter)
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """
        Search for similar documents in the vector store and return scores.
        
        Args:
            query: Query string
            k: Number of results to return
            filter: Filter to apply to the search
            
        Returns:
            List of tuples of (document, score)
        """
        return self.vectorstore.similarity_search_with_score(query=query, k=k, filter=filter)
    
    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search for documents using maximal marginal relevance.
        
        Args:
            query: Query string
            k: Number of results to return
            fetch_k: Number of results to fetch before filtering
            lambda_mult: Lambda multiplier for MMR
            filter: Filter to apply to the search
            
        Returns:
            List of documents
        """
        return self.vectorstore.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k,
            lambda_mult=lambda_mult,
            filter=filter
        )
    
    def delete(self, ids: List[str]) -> None:
        """
        Delete documents from the vector store.
        
        Args:
            ids: List of IDs to delete
        """
        self.vectorstore.delete(ids=ids)
    
    def persist(self) -> None:
        """Persist the vector store to disk."""
        self.vectorstore.persist()
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        client = self.vectorstore._client
        collection = client.get_collection(name=self.vectorstore._collection.name)
        return {
            "count": collection.count(),
            "name": collection.name,
        }