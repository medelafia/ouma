
kubectl delete -f k8s/mysql/Service.yaml
kubectl delete -f k8s/mysql/Deployment.yaml
kubectl delete -f k8s/mysql/PresistenceVolume.yaml 
kubectl delete secret mysql-secret --namespace monitoring

kubectl delete secret influxdb-auth --namespace monitoring
helm uninstall influxdb --namespace monitoring

kubectl delete secret ouma-secret --namespace monitoring
kubectl delete secret ouma-ui-secret --namespace monitoring

kubectl delete -f k8s/ouma/Service.yaml
kubectl delete -f k8s/ouma/Deployment.yaml
kubectl delete -f k8s/ouma/Ingress.yaml

kubectl delete -f k8s/ouma-ui/Service.yaml
kubectl delete -f k8s/ouma-ui/Deployment.yaml