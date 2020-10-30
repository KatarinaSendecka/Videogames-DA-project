## Required python modules

Install the following python modules using `pip install`

* pandas
* sqlalchemy
* psycopg2

The python 3 is required of at most 3.8 version. Warning, at the time when this
project was composed, the `psycopg2` dependency did not support python 3.9+. If you
encounter problems with those please try lower python minor version.

## Download for Murders dataset
https://drive.google.com/file/d/1AVcAEHfCAceagKkXSwCa8DI5k4prRIqT/view?usp=sharing 

## Running the conversion script

To see all the available options of the python script, run
```
python3 CSVimport.py --help
```

To start conversion into CSV files, simply run the command without parameters
```
python3 CSVimport.py
```

If you have a postgres database available on localhost:5432 running, you can let the
script create the database tables running the following
```
python3 CSVimport.py --init-db
```

To print informative output of the composed CSV files, use the following
```
python3 CSVimport.py --print-data
```

## Closing and starting docker database

* `docker ps` and copy **CONTAINER ID**
* `docker rm -f CONTAINER ID` - to close the database
* run in terminal: ./pgDocker.bat - to start the database
* run .\CSVimport.py 
