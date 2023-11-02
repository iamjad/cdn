import json
from flask import Flask, render_template, request, Response
import requests
import hashlib
import os

app = Flask(__name__)

origin_servers = {
    "github.mycdn.com:8080": {
        "origin": "avatars.githubusercontent.com",
        "protocal": "https"
    },
    "google.mycdn.com:8080": {
        "origin": "www.google.com",
        "protocal": "https"
    }
}

cache_directory = '/tmp/.cache_dir'

if not os.path.exists(cache_directory):
    os.makedirs(cache_directory)
    print(f"Directory '{cache_directory}' created.")
else:
    print(f"Directory '{cache_directory}' already exists.")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def getfile(path):

    if path == "favicon.ico": # ignore favicon request from browser
        return f''

    origin_url_path = get_path(request, path)
    # concatenate the cache directory with the hash of the origin url path.
    contents_file_path_on_the_disk = cache_directory + "/" + hashlib.sha256(origin_url_path.encode()).hexdigest()
    headers_file_path_on_the_disk = cache_directory + "/" + hashlib.sha256(os.path.join(origin_url_path, "_headers").encode()).hexdigest()
    # check if the file exists on the disk
    if os.path.exists(contents_file_path_on_the_disk):
        try:
            flask_response = None
            with open(contents_file_path_on_the_disk, 'rb') as file:
                file_content = file.read()
                flask_response = Response(file_content)
            
            with open(headers_file_path_on_the_disk, 'r') as headers_file:
                headers_text = headers_file.read()
                flask_response.headers['Content-Type'] = headers_text
            return flask_response
        except FileNotFoundError:
            print("File not found")

    # download and store on the disk
    response = requests.get(origin_url_path)
    if response.status_code == 200:
        write_contents_to_disk(contents_file_path_on_the_disk, response.content)
        write_headers_to_disk(headers_file_path_on_the_disk, response.headers['Content-Type'])
        return Response(response.content, headers={'Content-Type': response.headers['Content-Type']})
    else:
        return f'Hello from the default route! Route path: {path}'

def get_path(request, path):
    query_params = request.query_string.decode('utf-8')
    if query_params:
        query_params = "?" + query_params
    origin_url_path = str(origin_servers[request.host]["protocal"] + "://" +
                          origin_servers[request.host]["origin"] + "/" + path + query_params)
                          
    return origin_url_path


def write_contents_to_disk(file_path, contents):
    with open(file_path, "wb") as file:
        file.write(contents)

def write_headers_to_disk(file_path, headers):
    with open(file_path, "w") as file:
        file.write(headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
