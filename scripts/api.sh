#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

PORT=${API_PORT:-8000}
# Run the FastAPI application
poetry run uvicorn src.api.app:app --host 0.0.0.0 --port "$PORT"