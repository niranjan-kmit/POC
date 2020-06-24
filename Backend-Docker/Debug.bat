docker build -f Dockerfile -t gharikrishna123/pushpinbackend:v5 .
docker push gharikrishna123/pushpinbackend:v5
kubectl rollout restart deployment pushpin-backend
kubectl port-forward deployment/pushpin-dep 7999:7999 5561:5561 9390:9390 8006:8006 9090:9090