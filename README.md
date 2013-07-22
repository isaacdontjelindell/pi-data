pi-data
=======

Data logging project using a serial interface to the Raspberry Pi

db schema
---------
CREATE TABLE example (
    data VARCHAR(100),
    remotedatetime DATETIME,
    uploaded TINYINT(1)
);

