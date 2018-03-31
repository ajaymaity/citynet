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

Run an interactive shell inside the docker
-----
* for development
```
dev/run_dev_docker.sh 
```
* for production
```
prod/prod_run_docker.sh
```


Running Servers locally
======
Start a demo in Dev mode. 
------
Run inside the dev docker:
* import / create database
```
dev/create_dev_db.sh dump.sql
```
* Run all the servers and workers
```
./demo_psql.sh
```
Go to [localhost:8000](http://localhost:8000) in browser.


Start in Prod mode. 
------
* Run the docker for production-
```
docker/prod_run_docker.sh
```
* Run following command for creating the database -
```
prod/create_prod_db.sh
```
* Setup the nginx server by typing the following command-
```
prod/setup_nginx.sh local
```
* Start the prod server by typing the following command-
```
prod/start_dev.sh
```
Now access the server by typing [localhost](http://localhost) in browser.
This will block the terminal until the server is stopped with CTRL+C


Make documentation
====
Run the following commands:
```
docker/run_inside_docker.sh bash -c "cd doc; make html"
Then browse the file `doc/build/html/index.html`
``` 

