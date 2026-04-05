# Use the official uv image for a fast, reproducible build
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation and use copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy only what's needed for the dependency sync (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
# Removed --mount to ensure compatibility with GCP Cloud Build
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Expose FastAPI's default port
EXPOSE 8000

# Use 'uv run' to ensure the virtual environment is used
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
