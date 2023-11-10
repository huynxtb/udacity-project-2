dockerpath="noahgift/flasksklearn"

echo "Docker Image: $dockerpath"
docker login &&\
    docker image tag flasksklearn $dockerpath

docker image push $dockerpath 
