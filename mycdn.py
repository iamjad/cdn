from flask import Flask, render_template, request, Response
import requests
# import connexion
# app = connexion.App(__name__, specification_dir="./")
#app.add_api("swagger.yml")

app = Flask(__name__)

origin_servers = {
    "www.githubfileexample.com:8080": {
        "origin":"avatars.githubusercontent.com",
        "protocal": "https"
    },
    "www.googledynamicexample.com:8080" : {
        "origin":"www.google.com",
        "protocal": "https"
    }
}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def getfile(path):
    query_params = request.query_string.decode('utf-8')
    if query_params:
        query_params = "?" + query_params
    origin_url_path = str(origin_servers[request.host]["protocal"] + "://" + origin_servers[request.host]["origin"] + "/" + path + query_params)
    response = requests.get(origin_url_path)
    if response.status_code == 200:
        return Response(response.content, content_type=response.headers['Content-Type'])
    else:
        return f'Hello from the default route! Route path: {path}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)