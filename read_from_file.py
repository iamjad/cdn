import json
from flask import Flask, render_template, request, Response
import requests
import hashlib
import os

app = Flask(__name__)
@app.route('/fetch_and_store_google_search', methods=['GET'])
def fetch_and_store_google_search():
    url = 'https://www.google.com/search?q=chocolate'
    
    # Sending a GET request to Google and saving the response
    response = requests.get(url)
    
    # Create a filename to store the response and headers
    contents_file = 'google_search_response.html'
    
    # Save the response content to a file
    with open(contents_file, 'wb') as file:
        file.write(response.content)
    
    # Save the response headers to a separate file
    headers_filename = 'google_search_headers.txt'
    with open(headers_filename, 'w') as headers_file:
        headers_file.write(response.headers['Content-Type'])

    # Read the response content from the file
    with open(contents_file, 'rb') as file:
        content = file.read()
    
    # Read the response headers from the file
    with open(headers_filename, 'r') as headers_file:
        headers_text = headers_file.read()
    
    # Create a Flask response with the content and headers
    flask_response = Response(content)
    flask_response.headers['Content-Type'] = headers_text
        
    print(flask_response.headers['Content-Type'])
    # Return the Flask response
    # delete this file from local disk
    os.remove(contents_file)
    os.remove(headers_filename)
    
    return flask_response