# YouTube Video Upload Automation Tool

## Overview

This project is a tool for automating the upload of videos to YouTube using the YouTube Data API. It leverages Flask for the web interface and Google API libraries for authentication and video upload. The tool reads video metadata from a text file and uploads the videos to YouTube Shorts.

## Features

- **OAuth2 Authentication**: Securely authenticate with Google using OAuth2.
- **Automated Video Upload**: Upload videos to YouTube Shorts with metadata from a text file.
- **Error Handling**: Basic error handling and logging for troubleshooting.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Cloud project with YouTube Data API enabled
- OAuth 2.0 Client ID and Client Secret from Google Cloud Console

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shivadebnathA6/YouTube-Automation-tool.git
   cd YouTube-Automation-tool
