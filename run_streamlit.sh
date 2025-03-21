#!/bin/bash

# Print versions and environment info
echo "Running Python version: $(python --version)"
echo "Running Streamlit version: $(python -m pip show streamlit | grep Version)"

# Run Streamlit with specific configuration for Replit
python -m streamlit run app.py \
  --server.headless=true \
  --server.enableCORS=true \
  --server.enableXsrfProtection=false \
  --server.address=0.0.0.0 \
  --server.port=8501 \
  --browser.serverAddress=0.0.0.0 \
  --browser.gatherUsageStats=false
