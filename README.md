# This is a simple application of a CDN server. 

mycdn has list of distributions and each distribution define origin server. The contents at the path are stored locally in the cached folder and if the contents are not found, mycdn will fetch it from the origin and stores locally before returning to the client.

For this exercise, let's profile pictures of github.com users from github CDN. github users profile pictures is available on https://avatars.githubusercontent.com/u/<userid>. Any request coming to mycdn at localhost:8080 will go to "avatars.githubusercontent.com" origin in case if the user image is not stored locally. 

## Before running, update /etc/hosts file with the following enteries

127.0.0.1 google.mycdn.com

127.0.0.1 github.mycdn.com

