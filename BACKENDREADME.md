## Setting up the Development Environment

### macOS

1. Open Terminal.
2. Check if Python is installed: `python3 --version`.
    - If Python is not installed, download and install it from the [official Python website](https://www.python.org/downloads/).
3. Check if pip is installed: `pip3 --version`.
    - If pip is not installed, install it by running the following command: `python3 -m ensurepip --upgrade`.
4. Navigate to the `BackEnd` directory: `cd BackEnd`.
5. Create a virtual environment: `python3 -m venv venv`.
6. Activate the virtual environment: `source venv/bin/activate`.
7. Install Flask: `pip install Flask`.
8. Install Flask-CORS: `pip install flask-cors`.
9. Start the server: `python3 server.py`.

### Windows

1. Open Command Prompt.
2. Check if Python is installed: `python --version`.
    - If Python is not installed, download and install it from the [official Python website](https://www.python.org/downloads/).
3. Check if pip is installed: `pip --version`.
    - If pip is not installed, install it by following the instructions [here](https://pip.pypa.io/en/stable/installing/).
4. Navigate to the `BackEnd` directory: `cd BackEnd`.
5. Create a virtual environment: `python -m venv venv`.
6. Activate the virtual environment: `venv\Scripts\activate`.
7. Install Flask: `pip install Flask`.
8. Install Flask-CORS: `pip install flask-cors`.
9. Start the server: `python server.py`.

### Check to see if server is running

1. Open POSTMAN software
2. Create a GET request to http://127.0.0.1:5000/api/hello
3. Verify a response similar to: 
{
    "message": "Hello from Flask!"
}
