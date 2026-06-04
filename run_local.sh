###############################################################################
####    Copy Right 2026 (C) Mohamed EL AFIA                             
####    script : setup_all.sh 
####    description : This script is responsible for running the application locally using docker compose
###############################################################################

source ./.virtualenv/bin/activate
docker compose up --build -d 
fastapi run app.py