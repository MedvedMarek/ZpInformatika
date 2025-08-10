SHOW DATABASES
USE AAPL_2;


SHOW TABLES FROM AAPL_2;
SHOW TABLE STATUS LIKE 'smart';
SHOW TABLE STATUS FROM AAPL_2;
DESCRIBE smart


SHOW TABLE STATUS LIKE 'smart';
DESCRIBE smart

-- vybratie datumov zo stlpca time
SELECT DISTINCT DATE(time) AS datumy
FROM smart;


SELECT 
    DATE(time) AS datum,
    MIN(time) AS otvorenie_burzy,
    MAX(time) AS uzavretie_burzy
FROM smart
GROUP BY DATE(time);


----------------------------------------------------------------------------------

SELECT 
    -- a.datum,
    a.otvorenie_burzy,
    c.volume AS uzavretie_volume,
    b.volume AS otvorenie_volume,
    -- b.open AS dnesna_otvaracia_cena,
    -- c.close AS vcrajsia_zatvaracia_cena,
    ROUND(b.open - LAG(c.close, 1, 0) OVER (ORDER BY a.datum),1) AS gap
FROM 
    (SELECT 
        DATE(time) AS datum,
        MIN(time) AS otvorenie_burzy,
        MAX(time) AS uzavretie_burzy
    FROM smart
    GROUP BY DATE(time)
    ) a
JOIN smart b ON a.otvorenie_burzy = b.time
JOIN smart c ON a.uzavretie_burzy = c.time
ORDER BY gap DESC
LIMIT 20;


----------------------------------------------------------------------------------

CREATE TABLE obchodna_strategia.gap (
    datum DATE,
    dnesna_otv_cena FLOAT,
    otv_volume INT,
    uza_volume INT,
    gap FLOAT,
    max_vs_otv FLOAT,
    min_vs_otv FLOAT
);


-- ulozenie tabulky do databazy
INSERT INTO obchodna_strategia.gap (
    datum,
    dnesna_otv_cena,
    otv_volume,
    uza_volume,
    gap,
    max_vs_otv,
    min_vs_otv
)


-- vypocitanie gapu a vypocitanie rozdielu min a max ceny oproti otvaracej cene.
SELECT 
    -- a.datum,
    a.otvorenie_burzy,
    b.open AS dnesna_otv_cena,
    b.volume AS otv_volume,
    c.volume AS uza_volume,
    ROUND(b.open - LAG(c.close, 1, 0) OVER (ORDER BY a.datum), 1) AS gap,
    ROUND(MAX(d.high) - b.close, 1) AS max_vs_otvaracia,
    ROUND(MIN(d.low) - b.close, 1) AS min_vs_otvaracia
FROM 
    (SELECT 
        DATE(time) AS datum,
        MIN(time) AS otvorenie_burzy,
        MAX(time) AS uzavretie_burzy
    FROM smart
    GROUP BY DATE(time)
    ) a
JOIN smart b ON a.otvorenie_burzy = b.time
JOIN smart c ON a.uzavretie_burzy = c.time
JOIN smart d ON DATE(d.time) = a.datum
GROUP BY a.datum, a.otvorenie_burzy, b.open, b.volume
-- ORDER BY gap desc
-- limit 30;
order by datum asc;



--------------------------------------------------------------------------------------------
use obchodna_strategia;
show tables from obchodna_strategia;
show table status from obchodna_strategia;
show table status like 'gap';
describe gap;


select * from gap
where gap > 1.5
order by gap desc;
