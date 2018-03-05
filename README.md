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


Running Servers locally
======
Start a demo in Dev mode. 
------
Run demo.sh which will ask to setup
the project in development mode and then the project can be run on localhost
by typing [localhost:8000](http://localhost:8000) in browser.

```
docker/interactive_docker.sh
./demo.sh
```

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

<!--
Run frontend
======

Run the server
```
frontend/run-fe-docker.sh
```

Run Node realtime server
======

Run the server
```
frontend/run-fe-docker.sh
```
--status>

Make documentation
====
Run the following commands:
```
docker/run_inside_docker.sh bash -c "cd doc; make html"
Then browse the file `doc/build/html/index.html`
``` 

Install the Cityback Python package in development mode
======

``` 
pip3 install -e cityback
```

Celery Task demo
======

* Make sure RAbbitMq server is Running `rabbitmq-server -detached` 
* Run `celery worker --loglevel=info -A cityback.data_scheduler.app  --beat`

Django server
======
Run the Django server
```
cityback/run-django-server.sh
```