# Use an official Python runtime as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install flask

# Expose port 8080
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
