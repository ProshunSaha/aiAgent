# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
# We use pip to install directly since we don't have uv in the container by default yet,
# or we can just install from requirements if we had them.
# For now, we'll install dependencies manually or assume a requirements.txt generation.
# Better: Just install the dependencies we know are needed.

RUN pip install --no-cache-dir google-genai==1.12.1 python-dotenv==1.1.0 fastapi uvicorn sqlalchemy psycopg2-binary

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV GEMINI_API_KEY=""

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
