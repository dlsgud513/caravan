# 1. Base Image
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# 2. Set Environment Variables
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# 3. Set Working Directory
WORKDIR /app

# 4. Install Dependencies
# Copy the requirements file into the container
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Application Code
# Copy the rest of the application source code into the container
COPY . .

# 6. Expose Port
# Expose the port the app runs on
EXPOSE 8000

# 7. Run Application
# Command to run the application using uvicorn
# We use 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
