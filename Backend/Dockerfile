# Use the official Python image with version 3.11
FROM python:3.9-slim-bullseye

# Set the working directory to /main/backend
WORKDIR /Backend

# Copy the local requirements.txt file to the container at /main/backend
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# install chromium dependencies for playwright
RUN playwright install --with-deps chromium

# Copy the contents of the local main directory to the container at /Backend
COPY . .

# Set environment variables
# ENV PYTHONUNBUFFERED=1
ENV APP_CONFIG_FILE=/Backend/instance/prod_config.py

# wait for the database to fully initialize
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Make start.sh executable
RUN chmod +x start.sh

EXPOSE 5000

# Command to run on container start
CMD ["./start.sh"]
