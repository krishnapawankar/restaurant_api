# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to start the server
CMD ["flask", "run", "--host=0.0.0.0"]
