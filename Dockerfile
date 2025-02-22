# Use Python 3.11 as specified in requirements
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY . .

# Configure Poetry to not create virtual environment inside container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN pip install -U pip setuptools \
    && poetry lock \
    && poetry install --no-root \
    && poetry install --extras server

# Expose the default port mentioned in README
EXPOSE 8000

# Command to run the server
CMD ["python", "main.py", "--server", "--host", "0.0.0.0", "--port", "8000"]
