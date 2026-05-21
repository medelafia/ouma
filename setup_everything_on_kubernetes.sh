## setup mysql database
kubectl create secret generic mysql-secret --from-env-file=.env --namespace monitoring
kubectl apply -f k8s/mysql/PresistenceVolume.yaml
kubectl apply -f k8s/mysql/Deployment.yaml
kubectl apply -f k8s/mysql/Service.yaml 
## Setup influxdb
kubectl create secret generic influxdb-auth --from-env-file=.env.influxdb2 --namespace monitoring
helm repo add influxdata https://helm.influxdata.com/
helm repo update
helm install influxdb influxdata/influxdb2 --set adminUser.existingSecret=influxdb-auth --namespace monitoring

## Setup ouma backend
