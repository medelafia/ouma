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
        helm upgrade --install mysql bitnami/mysql -n monitoring -f ./charts/mysql/values.yaml\
            --set auth.existingSecret=mysql-secret
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
        docker build -t ouma:latest .
        docker tag ouma:latest mohamedelafia/ouma:latest
        docker build -t ouma-ui:latest ./ouma-ui
        docker tag ouma-ui:latest mohamedelafia/ouma-ui:latest
        echo "⚒️⛏️✅ Build completed"
    else
        echo "⚒️⛏️❌ Ignoring building"
    fi
    ## Setup ouma backend
    echo "🆙 Startup Ouma backend ..."
    if kubectl get configmap ouma-config-map -n monitoring >/dev/null 2>&1; then 
        echo "Ouma config map already exists"
    else 
        kubectl create configmap ouma-config-map  --from-env-file=.env --namespace monitoring
    fi
    helm upgrade --install ouma charts/ouma-chart
    echo "✅ Ouma backend ready ..."
    ## Setup ouma frontend 
    echo "🆙 Startup Ouma frontend ..."
    if kubectl get secret ouma-ui-config-map -n monitoring >/dev/null 2>&1; then 
        echo "Ouma-ui config map already exists"
    else
        kubectl create configmap ouma-ui-config-ma --from-env-file=./ouma-ui/.env --namespace monitoring
    fi
    helm upgrade --install ouma-ui charts/ouma-ui-chart
    echo "✅ Ouma frontend ready ..."
    echo "✅✅✅ Done"
else 
    echo "❌ Before starting the setup, ensure that Docker, Kubernetes, and Helm are installed on your system.";
fi