# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
# Ensure uvicorn is included, either in this command or in your requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Command to run the Uvicorn server without SSL, for use behind Traefik or another reverse proxy
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]