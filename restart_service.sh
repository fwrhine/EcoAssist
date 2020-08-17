DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $(echo $DIR)
sudo docker-compose down --rmi all && sudo docker-compose up -d --force-recreate --remove-orphans
