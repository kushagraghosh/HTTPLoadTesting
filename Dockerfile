# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --trusted-host pypi.python.org requests

# Set the default command to run when the container starts

#Example of a load test to Google with 4 requests and a QPS of 2 requests per second
CMD ["python", "load_tester.py", "https://www.google.com/", "--num-requests", "4", "--qps", "2.0"]

#Example of a stress test to https://fireworks.ai/ with 20 requests and a QPS of 2 requests per second
#CMD ["python", "load_tester.py", "https://fireworks.ai/", "--test-type", "stress", "--num-requests", "20", "--qps", "2.0"]