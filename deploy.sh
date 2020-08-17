docker build --tag aghniaprawira/team-clueless:latest .
docker push aghniaprawira/team-clueless:latest
scp -i team-clueless.pem ./docker-compose.yml ./restart_service.sh ubuntu@18.216.185.212:/home/ubuntu/team-clueless
ssh -i team-clueless.pem ubuntu@18.216.185.212 bash team-clueless/restart_service.sh
