## Required python modules

Install the following python modules using `pip install`

* pandas
* seaborn
* sqlalchemy
* psycopg2

## Download for Murders dataset
https://drive.google.com/file/d/1AVcAEHfCAceagKkXSwCa8DI5k4prRIqT/view?usp=sharing 

# Docker
To provide a database to the transformation scritp there're a few docker scripts that set it up.
To work with these, the [docker] needs to be installed.

## Starting a database
In terminal, run the following command inside the repository directory

### Windows
```
./pgDocker.bat
```
### Unix
```
./pgDocker.sh
```

The above will start new container callled `Videogames-DA-DB`. The container will have the standard postgresql
port forwarded to the host machine, therefore the database will be available on localhost:5432.

### Closing and starting new docker database with data

* `docker ps` and copy **CONTAINER ID**
* `docker rm -f CONTAINER ID` - to close the database
* run in terminal: ./pgDocker.bat - to start the database
* run .\CSVimport.py

### Storing database with fresh data

To avoid long repetitive insertion of the CSV data into the database tables every time a fresh docker container
is started, it is possible to store a snapshot of a freshly provisiioned database. This can be done using a
`docker commit` command. The following steps can be done to save freshly stored DB into a named docker container:

```
.\pgDocker.bat
python3 .\CSVimport.py
docker commit Videogames-DA-DB czechitas:db-loaded
```

Once the above is done, the freshly loaded database can be launched any time:
```
docker run --name czechitas-fresh -p 5432:5432 -d czechitas:db-loaded
```

note: Remember, that you can only have a single application running on the same port. For that reason,
there must be no other database docker container running at the time you launch the `czechitas:db-loaded`.
Alternatively, you may change the `-p` parameter attribute to start parallel database on a different port,
e.g. `-p 5433:5432` will forward the database port `5432` to a `localhost:5433`.

[docker]: https://www.docker.com/
