DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $(echo $DIR)
sudo docker-compose -f docker-compose.prod.yml down --rmi all && sudo docker-compose -f docker-compose.prod.yml up -d --build --force-recreate --remove-orphans
