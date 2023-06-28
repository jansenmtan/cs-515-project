# cs-515-project

![image](https://github.com/jansenmtan/cs-515-project/assets/36340429/e77bed47-278f-44be-8bda-014843662d8d)


## Required software
- [Python 3](https://www.python.org/)
  - [pip](https://pip.pypa.io/en/stable/installation/)
- [MariaDB](https://mariadb.org/)/[MySQL](https://www.mysql.com/)
  - [mysqlclient](https://github.com/PyMySQL/mysqlclient)
    - Follow the README to install.

## Setup
- Install all [required software](#required-software).
- Set up MariaDB/MySQL.
  - Create a new database for the project's use.
  - Edit `my.cnf` to set the database name, username, password, host, and port.
- Install required Python packages. 
```
pip install .
```
- Initialize server 
```
python airline/manage.py migrate
```
- Run the server 
```
python airline/manage.py runserver
```
- Go to https://127.0.0.1:8000/

