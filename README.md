Install git commit hooks
========================
```
  cd .git/hooks
  ln -s ../../.pre-commit pre-commit
```

Docker
======
Install docker from this [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/#prerequisites).
Once the package is install, follow the second [step](https://docs.docker.com/install/linux/linux-postinstall/).

Pull the docker image
----
```
docker pull asegroup11/all_servers:citynet
```

Build the docker image
-----
```
cd docker
./build.sh

```

Run a command inside the docker
-----
```
docker/run_inside_docker.sh python test/test.py 
```

Run an interactive shell inside the docker
-----
```
docker/interactive_docker.sh
```


PostgresSQL DB
======
Create db
------
```
docker/db_create.sh 
```

Run db
------
This will block the terminal until the server is stopped with CTRL+C
``` 
docker/db_run.sh
```


Run front-end
======
Run the server
```
front-end/run-fe-docker.sh
```


Make documentation
====
Run the following commands:
```
docker/run_inside_docker.sh bash -c "cd doc; make html"
```
Then browse the file `doc/build/html/index.html`