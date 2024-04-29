FROM python:3.8-slim

# Set working directory
WORKDIR /app

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY engine.py .

# Set the command to run your script
CMD ["python", "engine.py"]
