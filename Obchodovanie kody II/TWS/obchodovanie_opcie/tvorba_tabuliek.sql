use x_AAPL;
use x_ADBE;
use x_AMD;
use x_AMZN;
use x_ARM;
use x_BABA;
use x_DELL;
use x_GOOGL;
use x_MSFT;
use x_MU;
use x_ORCL;
use x_SNOW;
use x_SPY;
use x_TSLA;
use x_TSM;


create table arca (time integer primary key, volume integer);
create table bats (time integer primary key, volume integer);
create table drctedge (time integer primary key, volume integer);
create table edgea (time integer primary key, volume integer);
create table iex (time integer primary key, volume integer);
create table memx (time integer primary key, volume integer);
create table nasdaq (time integer primary key, volume integer);
create table nyse (time integer primary key, volume integer);
create table pearl (time integer primary key, volume integer);
create table psx (time integer primary key, volume integer);
create table smart (time integer primary key, open float, high float, low float, close float, volume integer);




use MSFT;

truncate table arca;
truncate table bats;
truncate table drctedge;
truncate table edgea;
truncate table iex;
truncate table memx;
truncate table nasdaq;
truncate table nyse;
truncate table pearl;
truncate table psx;
truncate table smart;


