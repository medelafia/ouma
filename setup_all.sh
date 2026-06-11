###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    script : setup_all.sh 
####    description : This script is responsible for setup the entire application and their dependancies on kubernetes cluster (databases, prometheus, ...)                           
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
    if kubectl get namespace monitoring >/dev/null 2>&1; then
        echo "🦈✅ Monitoring namespace already exists"
    else    
        kubectl create namespace monitoring
    fi

    if kubectl get svc prometheus-kube-prometheus-prometheus -n monitoring >/dev/null 2>&1; then
        echo "🦈✅ Prometheus service already exists"
    else 
        echo "🦈 Creating prometheus service ..."
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        helm repo update

        helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring
        echo "🦈✅ Prometheus service created successfully"
    fi

    if kubectl get svc mysql-service -n monitoring >/dev/null 2>&1; then 
        echo "🦈✅ Mysql service already exists"
    else
        echo "🦈 Creating mysql service ..."
        kubectl create configmap mysql-config-map --from-env-file=.env.mysql --namespace monitoring
        kubectl apply -f ./charts/mysql/Storage.yaml
        kubectl apply -f ./charts/mysql/DeploymentService.yaml
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
        helm install influxdb influxdata/influxdb2 \
        --set adminUser.existingSecret=influxdb-auth \
        --set service.port=8086 \
        --set influxdb.initOrg="oumaGuard-org"\
        --namespace monitoring
        echo "📈✅ Influx service created successfully"
    fi 

    read -p "do you want to build the images(y/n): " need_build
    ## build backend and frontend images 
    if [[ "$need_build" == "y" || "$need_build" == "Y" ]]; then
        echo "⚒️⛏️ Building images"
        docker build -t oumaGuard:latest .
        docker tag oumaGuard:latest mohamedelafia/oumaGuard:latest
        docker push mohamedelafia/oumaGuard:latest

        docker build -t oumaGuard-ui:latest ./oumaGuard-ui
        docker tag oumaGuard-ui:latest mohamedelafia/oumaGuard-ui:latest
        docker push mohamedelafia/oumaGuard-ui:latest
        echo "⚒️⛏️✅ Build completed"
    else
        echo "⚒️⛏️❌ Ignoring building"
    fi
    ## Setup ouma backend
    echo "🆙 Startup OumaGuard backend ..."
    if kubectl get configmap oumaGuard-config-map -n monitoring >/dev/null 2>&1; then 
        echo "OumaGuard config map already exists"
    else 
        kubectl create configmap oumaGuard-config-map  --from-env-file=.env --namespace monitoring
    fi

    helm upgrade --install oumaGuard charts/oumaGuard-chart -n monitoring
    echo "✅ OumaGuard backend ready ..."
    #Setup ouma frontend 
    echo "🆙 Startup OumaGuard frontend ..."

    if kubectl get configmap oumaGuard-ui-config-map -n monitoring >/dev/null 2>&1; then 
        echo "OumaGuard-ui config map already exists"
    else
        echo "waiting for oumaGuard's external IP" 
        while true; do
            IP_ADD=$(kubectl get svc -n monitoring \
                | grep oumaGuard-oumaGuard-chart \
                | awk '{print $4}')

            if [[ "$IP_ADD" != "<pending>" && -n "$IP_ADD" ]]; then
                break
            fi
            echo "."
            sleep 5
        done

        echo "External IP found: $IP_ADD"
        IP_ADD = kubectl get svc -n monitoring | grep oumaGuard-oumaGuard-chart | awk '{print $4}'
        kubectl create configmap oumaGuard-ui-config-map --from-literal=NEXT_PUBLIC_API_URL="http://$IP_ADD:8000" --namespace monitoring
    fi

    helm upgrade --install oumaGuard-ui charts/oumaGuard-ui-chart
    echo "✅ OumaGuard frontend ready ..."
    echo "✅✅✅ Done"
else 
    echo "❌ Before starting the setup, ensure that Docker, Kubernetes, and Helm are installed on your system.";
fi
