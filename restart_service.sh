sudo docker-compose -f docker-compose.prod.yml down --rmi all
sudo docker-compose -f docker-compose.prod.yml up -d --build --force-recreate --remove-orphans --scale redis-master=1 --scale redis-replica=3 --scale web=3 --scale nginx=1
