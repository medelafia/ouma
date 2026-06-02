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
        helm install influxdb influxdata/influxdb2 --set adminUser.existingSecret=influxdb-auth --set service.port=8086 --namespace monitoring
        echo "📈✅ Influx service created successfully"
    fi 

    read -p "do you want to build the images(y/n): " need_build
    ## build backend and frontend images 
    if [[ "$need_build" == "y" || "$need_build" == "Y" ]]; then
        echo "⚒️⛏️ Building images"
        eval $(minikube docker-env)
        docker build -t ouma:latest .
        docker build -t ouma-ui:latest ./ouma-ui
        echo "⚒️⛏️✅ Build completed"
    else
        echo "⚒️⛏️❌ Ignoring building"
    fi
    ## Setup ouma backend
    echo "🆙 Startup Ouma backend ..."
    if kubectl get secret ouma-secret -n monitoring >/dev/null 2>&1; then 
        echo "Ouma secret already exists"
    else 
        kubectl create secret generic ouma-secret --from-env-file=.env --namespace monitoring
    fi
    kubectl apply -f k8s/ouma/Deployment.yaml
    kubectl apply -f k8s/ouma/Service.yaml
    kubectl apply -f k8s/ouma/Ingress.yaml
    echo "✅ Ouma backend ready ..."
    ## Setup ouma frontend 
    echo "🆙 Startup Ouma frontend ..."
    if kubectl get secret ouma-ui-secret -n monitoring >/dev/null 2>&1; then 
        echo "Ouma-ui secret already exists"
    else
        kubectl create secret generic ouma-ui-secret --from-env-file=./ouma-ui/.env --namespace monitoring
    fi
    kubectl apply -f k8s/ouma-ui/Deployment.yaml
    kubectl apply -f k8s/ouma-ui/Service.yaml
    echo "✅ Ouma frontend ready ..."
    echo "✅✅✅ Done"
else 
    echo "❌ Before starting the setup, ensure that Docker, Kubernetes, and Helm are installed on your system.";
fi 