# Base image for Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install pipenv and project dependencies
RUN pip install pipenv && pipenv install --system --deploy

# Copy all the activities into the container
COPY activity /usr/src/app/activities/activity

# Copy the entrypoint script
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Expose the port the app will run on (adjust as needed)
EXPOSE 3000

# Default command to run the entrypoint script
CMD ["/usr/src/app/entrypoint.sh"]
