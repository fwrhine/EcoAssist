docker build --file ./services/web/Dockerfile.prod --tag aghniaprawira/team-clueless:latest .
echo "here"
docker build --file ./services/nginx/Dockerfile --tag aghniaprawira/team-clueless:nginx .
docker push aghniaprawira/team-clueless:latest
docker push aghniaprawira/team-clueless:nginx
scp -r -i team-clueless.pem ./services/web ubuntu@18.216.185.212:/home/ubuntu/team-clueless
scp -i team-clueless.pem ./docker-compose.prod.yml ./restart_service.sh ./.env.prod ./.env.prod.db ubuntu@18.216.185.212:/home/ubuntu/team-clueless
ssh -i team-clueless.pem ubuntu@18.216.185.212 bash team-clueless/restart_service.sh
