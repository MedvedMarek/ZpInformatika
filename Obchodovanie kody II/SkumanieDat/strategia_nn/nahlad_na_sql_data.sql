-- Tu je iba nahlad na data v sql. Nahlad je na rozne strategie ktore su
-- viazane na okolia. Pozera sa tu na pocet pripadov, ktore by boli pouzite
-- v nn trenovani.

show databases
use obchodna_strategia;

show tables from obchodna_strategia;


select * from aapl_okolie_12
where pr > 0.95
and suma > 20
order by pr desc;


select sum(suma) as celkova_suma from aapl_okolie_18
where pr > 0.9
and suma > 20
order by pr desc;



