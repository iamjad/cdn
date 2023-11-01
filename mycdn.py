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

    query_params = request.query_string.decode('utf-8')
    if query_params:
        query_params = "?" + query_params
    origin_url_path = str(origin_servers[request.host]["protocal"] + "://" +
                          origin_servers[request.host]["origin"] + "/" + path + query_params)
    sha256_hash = hashlib.sha256(origin_url_path.encode()).hexdigest()

    file_path_on_the_disk = cache_directory + "/" + sha256_hash
    if os.path.exists(file_path_on_the_disk):
        try:
            with open(file_path_on_the_disk, 'r') as file:
                file_content = file.read()
                return Response(file_content, content_type={'Content-Type': 'text/html; charset=ISO-8859-1'}) # hard coding for prototyping, headers should be cached and returned in the response.
        except FileNotFoundError:
            print("File not found")

    # download and store on the disk
    response = requests.get(origin_url_path)
    if response.status_code == 200:
        write_to_disk(file_path_on_the_disk, response)
        return Response(response.content, content_type=response.headers['Content-Type'])
    else:
        return f'Hello from the default route! Route path: {path}'


def write_to_disk(file_path, response):
    with open(file_path, "w") as file:
        file.write(response.content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
