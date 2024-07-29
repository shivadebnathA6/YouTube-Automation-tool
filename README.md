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

### Google Developer Console Setup

1. **Create a Google Cloud Project**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on **Select a Project** at the top of the page.
   - Click **New Project** and enter a name for your project.
   - Click **Create**.

2. **Enable the YouTube Data API**

   - In the Google Cloud Console, select your project.
   - Navigate to **APIs & Services** > **Library**.
   - Search for "YouTube Data API v3" and click on it.
   - Click **Enable**.

3. **Create OAuth 2.0 Credentials**

   - Navigate to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** and select **OAuth 2.0 Client ID**.
   - Configure the OAuth consent screen if you haven’t already:
     - Click **OAuth consent screen** in the sidebar.
     - Select **External** and click **Create**.
     - Fill in the required fields and click **Save and Continue**.
   - Go back to **Credentials** and click **Create Credentials** > **OAuth 2.0 Client ID**.
   - Select **Web application**.
   - Under **Authorized redirect URIs**, add the following URIs:
     - `http://localhost:8080/oauth2callback`
   - Click **Create**.
   - Download the `client_secret.json` file and save it to your project directory.

4. **Set Up OAuth 2.0 Scopes**

   - Make sure your OAuth consent screen includes the required scopes for accessing YouTube Data API.

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shivadebnathA6/YouTube-Automation-tool.git
   cd YouTube-Automation-tool


