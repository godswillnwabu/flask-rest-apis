FROM python:3.13-slim

# expose ports for Flask app
EXPOSE 5000 5678

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Install debugpy for remote debugging
RUN pip install debugpy

# Copy application code
COPY . .

# Default command (overridden in docker-compose.yml)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


