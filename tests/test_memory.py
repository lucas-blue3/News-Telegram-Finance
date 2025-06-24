"""
Tests for the memory components.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from aletheia.memory.vector_store import VectorMemory
from aletheia.memory.relational_store import RelationalMemory, Asset


class TestVectorMemory(unittest.TestCase):
    """Tests for the VectorMemory component."""
    
    def setUp(self):
        """Set up the test environment."""
        # Mock the embedding function to avoid API calls during testing
        self.mock_embeddings = MagicMock()
        self.mock_embeddings.embed_documents.return_value = [[0.1, 0.2, 0.3]] * 5
        self.mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
        
        # Create a temporary directory for testing
        self.test_dir = "/tmp/aletheia_test_vectordb"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Initialize the vector memory with the mock embeddings
        with patch('chromadb.Client') as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance
            self.vector_memory = VectorMemory(
                collection_name="test_collection",
                persist_directory=self.test_dir,
                embedding_function=self.mock_embeddings
            )
    
    def test_add_texts(self):
        """Test adding texts to the vector store."""
        # Mock the add_texts method of the vectorstore
        self.vector_memory.vectorstore.add_texts = MagicMock(return_value=["id1", "id2", "id3"])
        
        # Add texts to the vector store
        texts = ["Text 1", "Text 2", "Text 3"]
        metadatas = [{"source": "test"} for _ in range(3)]
        ids = self.vector_memory.add_texts(texts=texts, metadatas=metadatas)
        
        # Check that the add_texts method was called with the correct arguments
        self.vector_memory.vectorstore.add_texts.assert_called_once_with(texts=texts, metadatas=metadatas, ids=None)
        
        # Check that the method returns the expected IDs
        self.assertEqual(ids, ["id1", "id2", "id3"])
    
    def test_add_documents(self):
        """Test adding documents to the vector store."""
        # Mock the add_documents method of the vectorstore
        self.vector_memory.vectorstore.add_documents = MagicMock(return_value=["id1", "id2"])
        
        # Create test documents
        documents = [
            Document(page_content="Document 1", metadata={"source": "test"}),
            Document(page_content="Document 2", metadata={"source": "test"})
        ]
        
        # Add documents to the vector store
        ids = self.vector_memory.add_documents(documents=documents)
        
        # Check that the add_documents method was called with the correct arguments
        self.vector_memory.vectorstore.add_documents.assert_called_once_with(documents=documents)
        
        # Check that the method returns the expected IDs
        self.assertEqual(ids, ["id1", "id2"])
    
    def test_similarity_search(self):
        """Test similarity search in the vector store."""
        # Mock the similarity_search method of the vectorstore
        mock_docs = [
            Document(page_content="Result 1", metadata={"source": "test"}),
            Document(page_content="Result 2", metadata={"source": "test"})
        ]
        self.vector_memory.vectorstore.similarity_search = MagicMock(return_value=mock_docs)
        
        # Perform a similarity search
        results = self.vector_memory.similarity_search(query="test query", k=2)
        
        # Check that the similarity_search method was called with the correct arguments
        self.vector_memory.vectorstore.similarity_search.assert_called_once_with(query="test query", k=2, filter=None)
        
        # Check that the method returns the expected documents
        self.assertEqual(results, mock_docs)
    
    def tearDown(self):
        """Clean up after the tests."""
        # Remove the temporary directory
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


class TestRelationalMemory(unittest.TestCase):
    """Tests for the RelationalMemory component."""
    
    def setUp(self):
        """Set up the test environment."""
        # Use an in-memory SQLite database for testing
        self.relational_memory = RelationalMemory(db_url="sqlite:///:memory:")
        
        # Create the tables
        self.relational_memory.create_tables()
    
    def test_add_asset(self):
        """Test adding an asset to the database."""
        # Create a mock session
        mock_session = MagicMock()
        self.relational_memory.get_session = MagicMock(return_value=mock_session)
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=None)
        
        # Create a mock asset
        mock_asset = MagicMock(spec=Asset)
        mock_asset.id = 1
        mock_asset.symbol = "AAPL"
        mock_asset.name = "Apple Inc."
        
        # Mock the add and commit methods
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        mock_session.refresh = MagicMock()
        
        # Mock the Asset constructor
        with patch('aletheia.memory.relational_store.Asset') as mock_asset_class:
            mock_asset_class.return_value = mock_asset
            
            # Add an asset to the database
            asset_data = {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "asset_type": "stock",
                "sector": "Technology",
                "industry": "Consumer Electronics"
            }
            result = self.relational_memory.add_asset(asset_data=asset_data)
            
            # Check that the Asset constructor was called with the correct arguments
            mock_asset_class.assert_called_once_with(**asset_data)
            
            # Check that the add method was called with the mock asset
            mock_session.add.assert_called_once_with(mock_asset)
            
            # Check that the commit method was called
            mock_session.commit.assert_called_once()
            
            # Check that the refresh method was called with the mock asset
            mock_session.refresh.assert_called_once_with(mock_asset)
            
            # Check that the method returns the mock asset
            self.assertEqual(result, mock_asset)
    
    def tearDown(self):
        """Clean up after the tests."""
        # Drop the tables
        self.relational_memory.drop_tables()


if __name__ == '__main__':
    unittest.main()