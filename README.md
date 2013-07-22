pi-data
=======

Data logging project using a serial interface to the Raspberry Pi

db schema
---------
    CREATE TABLE example (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        data VARCHAR(100),
        remotedatetime DATETIME,
        uploaded TINYINT(1),
        PRIMARY KEY (id)
    );


dependencies
------------
* mysqldb
* requests
* serial


TODO
----
* Time format? (UTC, tz, etc)
