"""
Script to run the Aletheia Streamlit app.
"""

import os
import subprocess
import sys

def main():
    """Run the Streamlit app."""
    # Ensure the required directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/vectordb", exist_ok=True)
    os.makedirs("aletheia/ui/components", exist_ok=True)
    
    # Set environment variables
    os.environ["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
    
    # Get the port from the environment or use default
    port = os.environ.get("PORT", "12000")
    
    # Run the Streamlit app
    cmd = [
        "streamlit", "run", "aletheia/ui/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "true",
        "--server.enableXsrfProtection", "false"
    ]
    
    print(f"Running Streamlit app on port {port}...")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()