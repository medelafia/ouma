###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    script : setup_all.sh 
####    description : This script is responsible for setup the entire application and their dependancies (databases, prometheus, ...)                           
###############################################################################


echo ""
echo "=============================================="
echo "=+  Kubernetes Full Stack Deployment Script +="
echo "=+  Setup: App + Databases + Monitoring     +="
echo "=+  Author: Mohamed EL AFIA (2026)          +="
echo "=============================================="
echo ""

### checking if the required commands exists (kubectl, docker and helm)
if command -v docker &> /dev/null && command -v helm &> /dev/null && command -v kubectl &> /dev/null; then
    ## setup mysql database 
    if kubectl get svc mysql-service -n monitoring >/dev/null 2>&1; then 
        echo "🦈✅ Mysql service already exists"
    else
        echo "🦈 Creating mysql service ..."
        kubectl create secret generic mysql-secret --from-env-file=.env.mysql --namespace monitoring
        kubectl apply -f k8s/mysql/PresistenceVolume.yaml
        kubectl apply -f k8s/mysql/Deployment.yaml
        kubectl apply -f k8s/mysql/Service.yaml 
        echo "🦈✅ Mysql service created successfully"
    fi
    ## Setup influxdb
    if kubectl get svc influxdb-influxdb2 -n monitoring >/dev/null 2>&1; then 
        echo "📈✅ InfluxDB service already exists"
    else
        echo "📈 Creating influxdb service ..."
        kubectl create secret generic influxdb-auth --from-env-file=.env.influxdb2 --namespace monitoring
        helm repo add influxdata https://helm.influxdata.com/
        helm repo update
        helm install influxdb influxdata/influxdb2 --set adminUser.existingSecret=influxdb-auth --namespace monitoring
        echo "📈✅ Influx service created successfully"
    fi 
    # appending the IPs of the related services to env file
    head -n $(($(wc -l < .env)-3)) .env > temp.env && mv temp.env .env
    echo "📝 Appending IPs addresses to the .env file ..."
    echo "TARGET_SERVER_HOST=$(kubectl get svc prometheus-kube-prometheus-prometheus --namespace monitoring | grep prometheus-kube-prometheus-prometheus | awk '{print $3}')" >> .env
    echo "MYSQL_HOST=$(kubectl get svc mysql-service --namespace monitoring | grep mysql-service | awk '{print $3}')" >> .env
    echo "INFLUX_DB_URL=$(kubectl get svc influxdb-influxdb2 --namespace monitoring | grep influxdb-influxdb2 | awk '{print $3}')" >> .env
    echo "📝✅ IPs Appended successfully"
    ## build backend and frontend images 
    docker build -t ouma:latest .
    docker build -t ouma-ui:latest ./ouma-ui

    #docker tag 

    ## Setup ouma backend
    echo "Setting up application backend ..."
    kubectl create secret generic ouma-secret --from-env-file=.env --namespace monitoring
    kubectl apply -f k8s/ouma/deployment.yaml
    kubectl apply -f k8s/ouma/service.yaml
    ## Setup ouma frontend 
    echo "Setting up application frontend ..."
    kubectl create secret generic ouma-ui-secret --from-env-file=./ouma-ui/.env --namespace monitoring
    kubectl apply -f k8s/ouma-ui/deployment.yaml
    kubectl apply -f k8s/ouma-ui/service.yaml
    echo "✅ Done"
else 
    echo "❌ Before starting the setup, ensure that Docker, Kubernetes, and Helm are installed on your system.";
fi 

