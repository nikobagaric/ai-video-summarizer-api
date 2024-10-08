# Video Summarizer App

## Introduction

This is the backend for a video summary project using the YouTube API. The app processes YouTube URLs to generate summaries of the video content and saves them as notes.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Docker Configuration](#docker-configuration)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Docker installed on your machine.
- You have your LangChain and OpenAI API keys prepared.
- You have Python 3.8 or higher installed if you plan to run the app outside of Docker.

## Installation

To set up the project, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/video-summarizer-app.git
    cd video-summarizer-app
    ```

2. **Create a `.env` file**:
    Create a `.env` file in the root directory of the project and add your environment variables (see [Environment Variables](#environment-variables) section).

3. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

## Usage

To use the app, follow these steps:

1. **Start the Docker containers**:
    ```sh
    docker-compose up
    ```

2. **Access the API**:
    The API will be available at `127.0.0.1:8000/api/docs/#/`.

3. **Process a YouTube URL**:
    Send a POST request to `/notes/process_youtube_url` with the YouTube URL in the request body:
    ```json
    {
        "url": "https://www.youtube.com/watch?v=example"
    }
    ```

## Environment Variables

The following environment variables need to be set in your `.env` file:

```env
    DB_HOST=db
    DB_NAME=devdb
    DB_USER=devuser
    DB_PASS=root
    DEBUG=1
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key
```

## Docker Configuration

The Docker setup includes the following services:

- **backend**: The main application service.
- **db**: PostgreSQL database service.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.