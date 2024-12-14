#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Apply database migrations
alembic upgrade head