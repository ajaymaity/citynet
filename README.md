Install git commit hooks
========================
```
  cd .git/hooks
  ln -s ../../.pre-commit pre-commit
```

Docker
======
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