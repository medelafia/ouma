kubectl delete -f k8s/mysql/Service.yaml
kubectl delete -f k8s/mysql/Deployment.yaml
kubectl delete -f k8s/mysql/PresistenceVolume.yaml 
kubectl delete secret mysql-secret --namespace monitoring

kubectl delete secret influxdb-auth --namespace monitoring
helm uninstall influxdb --namespace monitoring