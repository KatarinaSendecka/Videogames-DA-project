## Required python modules

Install the following python modules using `pip install`

* pandas
* sqlalchemy
* psycopg2

## Download for Murders dataset
https://drive.google.com/file/d/1AVcAEHfCAceagKkXSwCa8DI5k4prRIqT/view?usp=sharing 

## Closing and starting docker database

* `docker ps` and copy **CONTAINER ID**
* `docker rm -f CONTAINER ID` - to close the database
* run in terminal: ./pgDocker.bat - to start the database
* run .\CSVimport.py 