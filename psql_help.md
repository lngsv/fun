## Some useful commands for postgreSQL on macOS

### Install
```
$ brew install postgresql
$ brew services start postgresql
$ psql -l # maybe brew install libpq is needed to install psql
$ psql postgres
$ psql <DB_NAME> [<ROLE_NAME>]
```

### Create your own user and database
```
postgres=# CREATE USER <role_name> WITH password '<password>';
CREATE USER
postgres=# CREATE DATABASE <db_name> OWNER <role_name>;
CREATE DATABASE
```

### Some psql commands

* `\?` — показать список команд
* `\du` — показать список пользователей с привилегиями
* `\l` — показать список баз данных
* `\с db_name2` — подключиться к другой базе данных
* `\dt` — показать список таблиц
* `\d table_name` — показать колонки таблицы
* `\x` — переключить режим вывода
* `\q` — выход из psql
