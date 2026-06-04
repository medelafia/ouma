kubectl delete configmap mysql-config-map -n monitoring
kubectl delete -f ./charts/mysql/Storage.yaml
kubectl delete -f ./charts/mysql/DeploymentService.yaml

kubectl delete secret influxdb-auth -n monitoring
helm delete influxdb -n monitoring
kubectl delete configmap ouma-config-map -n monitoring

kubectl delete configmap ouma-config-map -n monitoring
helm delete ouma -n monitoring
