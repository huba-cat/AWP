# Use a basic Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install any Python packages (if needed)
# If you have requirements.txt, use this line:
# RUN pip install -r requirements.txt

# Otherwise, install manually:
RUN pip install requests

# Command to run your script
CMD ["python", "generate_sample_data.py"]
