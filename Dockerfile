# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Open port 8501 (Streamlit's default)
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "web_app.py"]