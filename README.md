# DECO3801 Team Clueless

##### To run locally:
```
$ docker-compose up -d --build
```
or
```
$ docker-compose down --rmi all && docker-compose up -d --build
```

Try it on: http://localhost:5000

or on Windows, get your docker machine ip from:
```
$ docker-machine ip
```

Then open: http://your_docker_machine_ip:5000
<br />
<br />

##### To connect to local postgresql database:

```
$ docker-compose exec db psql --username=team_clueless --dbname=team_clueless_dev
```
<br />

##### AWS server:

http://18.216.185.212:1337/
<br />
<br />

##### If you find this error ```standard_init_linux.go:211: exec user process caused "no such file or directory"```:

Try checking the line ending type of the file ```entrypoint.sh```.
If type is CRLF, change to LF.

![image](./LF.jpg?raw=true)
