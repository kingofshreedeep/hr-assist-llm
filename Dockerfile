# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY project/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make run.sh executable
RUN chmod +x scripts/run.sh

# Make ports available
EXPOSE 8501 8000

# Define environment variable
ENV STREAMLIT_SERVER.PORT 8501

# Run the application
CMD ["scripts/run.sh"]