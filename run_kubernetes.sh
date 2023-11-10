dockerpath="noahgift/flasksklearn"

kubectl run flaskskearlndemo\
    --generator=run-pod/v1\
    --image=$dockerpath\
    --port=80 --labels app=flaskskearlndemo

kubectl get pods

kubectl port-forward flaskskearlndemo 8000:80



