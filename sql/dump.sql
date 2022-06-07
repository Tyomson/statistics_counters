CREATE TABLE IF NOT EXISTS statistics (
    PRIMARY KEY (id),
    id                 INT(11)       NOT NULL AUTO_INCREMENT,
    created_dt          DATE         NULL,
    views              INT(4)        NULL,
    clicks             INT(4)        NULL,
    cost               DECIMAL(10,2) NULL,
    cpc                DECIMAL(10,2) NULL,
    cpm                DECIMAL(10,2) NULL
);
