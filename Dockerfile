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
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi \
    && /py/bin/pip install -U https://github.com/coletdjnz/yt-dlp-youtube-oauth2/archive/refs/heads/master.zip \
    && rm -rf /tmp \
    && adduser --disabled-password --no-create-home django-user

# Create the /videos directory and set the ownership before switching to the non-root user
RUN mkdir -p /videos && chown -R django-user:django-user /videos

# Switch to non-root user
USER django-user
