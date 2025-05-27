# NetShare

## Project Title

NetShare

## Description

NetShare is a simple, web-based application built with Flask that allows you to easily share files between devices on your local network. It provides a user-friendly interface for both sending and receiving files without the need for external services or complex configurations.

## Features

*   **Easy File Sending:** Select one or more files and send them to a target IP address on your local network.
*   **Simple File Receiving:** Start a receiver process to listen for incoming files and automatically save them to a designated folder.
*   **Web Interface:** A clean and intuitive web interface for managing file transfers.
*   **Activity Logging:** Keep track of sent and received files with a built-in activity log.
*   **Cross-Platform:** Built with Python, it should run on any operating system that supports Python and Flask.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.6 or higher
*   Flask library (`pip install Flask`)
*   `requests` library (`pip install requests`) - (Although `sender.py` uses sockets directly, Flask might have a dependency or it might be planned for future use in the web interface for more advanced sending features).
*   Font Awesome 5.15.3 (included via CDN in HTML)

### Installation

1.  **Clone the repository:**
```
bash
    git clone https://github.com/Adithya2369/Net-Share
    
```
2.  **Install dependencies:**
```
bash
    pip install -r requirements.txt
    
```
(Assuming you have a `requirements.txt` file listing Flask and requests. If not, manually install them: `pip install Flask requests`)

### Running the App

1.  **Navigate to the project directory:**
```
bash
    cd NetShare
    
```
2.  **Run the Flask application:**
```
bash
    python app.py
    
```
The application will start and be accessible at `http://<your_local_ip>:5000`.

## Usage

### Receiving Files

1.  Open the application in your web browser (e.g., `http://192.168.1.100:5000`).
2.  Click on "Receive Files".
3.  Click the "Start Listening" button. The application will start a receiver process that listens for incoming connections on port 5001.
4.  Received files will appear in the "Received Files" section and will be saved to the `downloads` folder in the project directory.
5.  Click "Stop Listening" to stop the receiver process.

### Sending Files

1.  Open the application in your web browser (e.g., `http://192.168.1.100:5000`).
2.  Click on "Send Files".
3.  Click "Choose Files" to select the files you want to send. You can select multiple files.
4.  Enter the IP address of the device that is running the NetShare receiver in the "Target IP Address" field.
5.  Click "Send Files". The application will send the selected files to the target IP address.

## Project Structure
```
NetShare/
├── app.py
├── app_functions.py
├── sender.py
├── receiver.py
├── activity.log
├── templates/
│   ├── index.html
│   ├── send.html
│   ├── receive.html
└── static/
    ├── css/
    │   └── style.css
    └── img/
        └── logo.png
```
*   **`app.py`:** The main Flask application file. Handles web routes, serves templates, and provides API endpoints.
*   **`app_functions.py`:** Contains helper functions used by `app.py` for managing the sender and receiver processes and logging activity.
*   **`sender.py`:** A standalone script for sending files over the network using sockets.
*   **`receiver.py`:** A standalone script that acts as a server to receive files over the network using sockets.
*   **`templates/`:** Contains the HTML files for the web interface.
    *   `index.html`: The main landing page.
    *   `send.html`: The page for sending files.
    *   `receive.html`: The page for receiving files.
*   **`static/`:** Contains static files like CSS and images.
    *   `css/style.css`: Custom CSS styles for the web interface.
    *   `img/logo.png`: The application logo.

## License

Copyright (c) 2025 T. Adithya Reddy

Permission is granted to use, copy, and distribute this software for any purpose, provided that the original author is credited.

Modification, alteration, or derivative works based on this software are NOT permitted without explicit written permission from the author.

No warranty is provided. Use at your own risk.
