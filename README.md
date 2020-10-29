# DECO3801 Team Clueless
A project by Team Clueless for DECO3801 Design Computing Studio.

![image](./EcoAssist.png?raw=true)

EcoAssist is a web application that aims to help teachers educate their students about the environment. 

##### Features:
- Teachers can assign environment-related tasks for students to complete.
- Students can complete these tasks, be awarded points, and ranked in a class leaderboard.
- Students can learn background information about the environment.
- Teachers can award badges for specific achievements.

##### Team Members:
1. Benjamin Costello (43931044)
2. Sean Lim Han Ming (45054965)
3. Aghnia Putri Prawira (45610240)
4. Rizki Maulana Rahmadi (45616747)
5. Alexander Bayusuto Waanegkirtyo (45616738)
6. Jordan Monroe (44785280)

---

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

http://18.216.185.212:5000/
<br />
<br />

##### If you find this error ```standard_init_linux.go:211: exec user process caused "no such file or directory"```:

Try checking the line ending type of the file ```entrypoint.sh```.
If type is CRLF, change to LF.

![image](./LF.jpg?raw=true)
