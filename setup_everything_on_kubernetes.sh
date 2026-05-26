## setup mysql database
echo "Creating mysql service ..."
kubectl create secret generic mysql-secret --from-env-file=.env --namespace monitoring
kubectl apply -f k8s/mysql/PresistenceVolume.yaml
kubectl apply -f k8s/mysql/Deployment.yaml
kubectl apply -f k8s/mysql/Service.yaml 
echo "Mysql service created successfully ..."
## Setup influxdb
echo "Creating influxdb service ..."
kubectl create secret generic influxdb-auth --from-env-file=.env.influxdb2 --namespace monitoring
helm repo add influxdata https://helm.influxdata.com/
helm repo update
helm install influxdb influxdata/influxdb2 --set adminUser.existingSecret=influxdb-auth --namespace monitoring
echo "Influx service created successfully"
# appending the IPs of the related services to env file
echo "Appending IPs addresses to the .env file ..."
if 
echo "TARGET_SERVER_HOST=$(kubectl get svc prometheus-kube-prometheus-prometheus --namespace monitoring | grep prometheus-kube-prometheus-prometheus | awk '{print $3}')" >> .env
echo "MYSQL_HOST=$(kubectl get svc mysql-service --namespace monitoring | grep mysql-service | awk '{print $3}')" >> .env
echo "INFLUX_DB_URL=$(kubectl get svc influxdb-influxdb2 --namespace monitoring | grep influxdb-influxdb2 | awk '{print $3}')" >> .env
echo "Appended successfully"
## Setup ouma backend
echo "Setting up application backend ..."
kubectl apply -f k8s/ouma/deployment.yaml
kubectl apply -f k8s/ouma/service.yaml
## Setup ouma frontend 
echo "Setting up application frontend ..."
kubectl apply -f k8s/ouma-ui/deployment.yaml
kubectl apply -f k8s/ouma-ui/service.yaml
echo "Done"