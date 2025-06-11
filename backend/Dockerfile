FROM python:3.11-slim

# Work directory
WORKDIR /app

COPY static ./static
COPY templates ./templates
COPY app.py /app

# Install lib
RUN pip install flask prometheus_client werkzeug flask-cors

# Create folder for uploads files
RUN mkdir uploads

# Open app port
EXPOSE 8000

# Run app
CMD ["python", "app.py"]
