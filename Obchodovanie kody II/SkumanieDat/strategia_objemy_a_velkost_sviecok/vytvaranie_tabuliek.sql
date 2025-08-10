SHOW DATABASES
SHOW TABLES FROM obchodna_strategia



USE AAPL_2;
DESCRIBE smart
SHOW TABLE STATUS FROM AAPL_2;
SHOW TABLE STATUS LIKE 'smart';
SHOW TABLE STATUS LIKE 'arca';


-------------------------------------------------------
--------------- vytvorenie tabulky --------------------
-------------------------------------------------------
-- vytvaranie tabulky v databaze pre zapisovanie z python
-- kodu.

aapl, amd, amzn, baba, googl, msft, orcl, spy, tsla, tsm


use obchodna_strategia;
show table status from obchodna_strategia;


CREATE TABLE tsm_okolie_12 (
    id int AUTO_INCREMENT PRIMARY KEY,
    burza varchar(255),
    ob_min int,
    ob_max int,
    sv_min float,
    sv_max float,
    `true` int,
    `false` int,
    suma int,
    pr float
);


-----------------------------------------------------
-------------- uz praca s datami --------------------
-----------------------------------------------------

USE obchodna_strategia;
SHOW TABLES FROM obchodna_strategia;
show table status from obchodna_strategia;
show table status like 'okolie_23';
DESCRIBE okolie_23;


select * from okolie_23
where pr > 0.95 and
suma > 20
order by pr desc;






