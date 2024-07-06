FROM python:3.11.9-slim

LABEL maintainer="Niko Bagaric"

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:/py/bin:$PATH"

# Copy requirements files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the application code and scripts
COPY ./scripts /scripts
COPY ./ai_notes /ai_notes

# Set the working directory
WORKDIR /ai_notes

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home django-user

# Switch to non-root user
USER django-user

# Define the default command to run the application
CMD ["run.sh"]