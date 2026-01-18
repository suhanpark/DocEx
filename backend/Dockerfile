FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .
COPY requirements.txt .

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . .

# Expose port for Render
EXPOSE 10000

# Run the application
CMD ["uv", "run", "python", "run.py"]
