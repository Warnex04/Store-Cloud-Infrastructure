# Use Python 3.11.5 as the base image
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Set default port and allow overriding with an environment variable)
ARG PORT=5000
ENV PORT ${PORT}
EXPOSE ${PORT}

# Set environment variables (add other commonly used environment variables as needed)
ENV KAFKA_BROKER_URL=kafka:9092
ENV MONGODB_URL=mongodb://mongo:27017/
ENV MONGODB_RECEIPTS_COLLECTION=receipts
ENV MONGODB_ALERTS_COLLECTION=alerts

# Define volumes for MongoDB data (for receipts and alerts)
VOLUME ["/data/db", "/data/configdb"]

# Run the application
CMD ["python", "./StoreProducer.py"]
