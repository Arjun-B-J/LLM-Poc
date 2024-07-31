Create schema coporate_bondsv2;
use coporate_bondsv2;
CREATE TABLE `offers` (
  `CUSIP` varchar(10) NOT NULL,
  `TIER` int DEFAULT NULL,
  `QUANTITY` int DEFAULT NULL,
  `PRICE` decimal(4,2) DEFAULT NULL,
  `BENCHMARK` varchar(45) DEFAULT NULL,
  `SPREAD` decimal(4,2) DEFAULT NULL,
  `DATE` datetime DEFAULT NULL,
  `AXE` tinyint DEFAULT NULL,
  `FIRM` tinyint DEFAULT NULL,
  `ACTIVE` int DEFAULT NULL,
  PRIMARY KEY (`CUSIP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `offers` VALUES ('084670BR8',1,44445,67.78,'TREAS',88.00,'2024-07-03 00:00:00',1,1,1),('084670BR9',1,14000,89.67,'TREAS',76.56,'2024-07-03 00:00:00',1,0,0),('172967FT3',2,23000,78.96,'TREAS',78.50,'2024-07-03 00:00:00',1,0,0),('172967FT4',2,45666,67.77,'TREAS',90.00,'2024-07-03 00:00:00',1,1,1),('20030NBP5',1,32003,98.75,'TREAS',70.00,'2024-07-03 00:00:00',0,1,0),('459200GJ4',1,30000,98.34,'TREAS',67.08,'2024-07-03 00:00:00',0,1,0),('50076QAZ9',2,24000,97.11,'TREAS',69.56,'2024-07-03 00:00:00',1,0,0),('59156RBB3',2,23000,89.34,'TREAS',78.88,'2024-07-03 00:00:00',1,0,0),('931142DH3',2,34555,78.88,'TREAS',79.00,'2024-07-03 00:00:00',1,0,0),('931142DH4',1,56777,78.88,'TREAS',81.00,'2024-07-03 00:00:00',1,0,1);

CREATE TABLE `security` (
  `CUSIP` varchar(10) NOT NULL,
  `DESCR` varchar(45) DEFAULT NULL,
  `TICKER` varchar(45) DEFAULT NULL,
  `COUPON` decimal(4,2) DEFAULT NULL,
  `OUTSTANDING` int DEFAULT NULL,
  `MATURITY` datetime DEFAULT NULL,
  `INDUSTRY` varchar(45) DEFAULT NULL,
  `RATING` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`CUSIP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `security` VALUES ('00206RCG5','AT&T','ATT',4.32,657780,'2024-07-03 00:00:00','Com','A'),('02079KAC1','Alphabet','GOOG',2.78,78990,'2024-07-03 00:00:00','Comm','A'),('060505DP6','Bank of America','BAC',3.21,46000,'2024-07-03 00:00:00','Fin','A++'),('084670BR8','Apple Inc','Apple Inc',5.60,6,'2024-07-03 00:00:00','IT','A'),('084670BR9','Apple Inc','Apple Inc',5.60,6,'2024-07-03 00:00:00','IT','A'),('14149YAZ1','Cardinal Health','CDH',2.90,12000,'2024-07-03 00:00:00','Health','B'),('172967FT3','CITI GROUP INC','CITI',3.44,67900,'2024-07-03 00:00:00','Fin','A'),('172967FT4','CITI GROUP INC','CITI',3.46,56800,'2024-07-03 00:00:00','Fin','A'),('20030NBP5','COMCAST CORP','CCC',3.56,45000,'2024-07-03 00:00:00','Pharma','A+'),('26442RAD3','Duke Energy INC','DUK',3.99,65990,'2024-07-03 00:00:00','Electric','B'),('459200GJ4','IBM Corp','IBM',4.01,34000,'2024-07-03 00:00:00','IT','A'),('478160BV5','Johnson & Johsnon','JNJ',5.34,445560,'2024-07-03 00:00:00','Retail','A'),('49326EE99','FEDEX Group','FED',4.10,67999,'2024-07-03 00:00:00','Com','A'),('50076QAZ9','Kraft H Foods','KFH',3.89,46000,'2024-07-03 00:00:00','Agro','A+'),('59156RBB3','MET LIFE','MET',3.44,88900,'2024-07-03 00:00:00','Insurance','A'),('929903DT6','Wachovia','WAC',3.89,45880,'2024-07-03 00:00:00','Fin','B'),('931142DH3','WallMart','WMT',3.67,56000,'2024-07-03 00:00:00','Retail','A'),('931142DH4','WallMart','WMT',3.65,67000,'2024-07-03 00:00:00','Retail','A');

CREATE TABLE `trades` (
  `ID` int NOT NULL,
  `CUSIP` varchar(10) DEFAULT NULL,
  `ECN` varchar(45) DEFAULT NULL,
  `QUANTITY` int DEFAULT NULL,
  `PRICE` decimal(4,2) DEFAULT NULL,
  `BENCHMARK` varchar(45) DEFAULT NULL,
  `DATE` datetime DEFAULT NULL,
  `STATUS` varchar(45) DEFAULT NULL,
  `DEALER` varchar(45) DEFAULT NULL,
  `CLIENT` varchar(45) DEFAULT NULL,
  `TIER` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `trades` VALUES (1,'931142DH3','MA',5000,69.90,'TREAS','2024-07-03 00:00:00','DONE','BLACKROCK','BLACKROCK',1),(2,'929903DT6','MA',5000,79.90,'TREAS','2024-07-03 00:00:00','DONE','ALIBABA','ALIBABA',1),(3,'59156RBB3','TW',6000,65.78,'TREAS','2024-07-03 00:00:00','LOST','SUBARU ','SUBARU ',2),(4,'50076QAZ9','TW',6000,89.60,'TREAS','2024-07-03 00:00:00','LOST','ATT','ATT',2),(5,'459200GJ4','BBG',6500,91.10,'TREAS','2024-07-03 00:00:00','DONE','ATT','ATT',3),(6,'26442RAD3','BBG',5600,78.56,'TREAS','2024-07-03 00:00:00','DONE','FRANKLIN','FRANKLIN',3),(7,'20030NBP5','NEP',4500,67.88,'TREAS','2024-07-03 00:00:00','LOST','FRANKLIN','FRANKLIN',1),(8,'02079KAC1','BBG',3400,67.88,'TREAS','2024-07-03 00:00:00','DONE','SBI','SBI',1),(9,'14149YAZ1','MA',4500,67.88,'TREAS','2024-07-03 00:00:00','DONE','SBI','SBI',1),(10,'931142DH3','MA',4500,67.88,'TREAS','2024-07-02 00:00:00','DONE','SBI','SBI',2),(11,'931142DH3','BBG',4500,67.88,'TREAS','2024-07-02 00:00:00','DONE','FRANKLIN','FRANKLIN',1),(12,'459200GJ4','TW',4500,78.56,'TREAS','2024-07-02 00:00:00','LOST','ATT','ATT',1),(13,'14149YAZ1','BBG',4500,78.56,'TREAS','2024-07-02 00:00:00','LOST','ATT','ATT',1),(14,'172967FT3','NEP',5600000,78.91,'TREAS','2024-07-02 00:00:00','DONE','GC','GC',1),(15,'084670BR9','MA',4455500,77.39,'TREAS','2024-07-02 00:00:00','DONE','GC','GC',1);
CREATE TABLE `trace` (
  `ID` int NOT NULL,
  `CUSIP` varchar(10) DEFAULT NULL,
  `DEALER` varchar(45) DEFAULT NULL,
  `QUANTITY` int DEFAULT NULL,
  `PRICE` decimal(4,2) DEFAULT NULL,
  `DATE` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `trace` VALUES (1,'02079KAC1','WFS',3400,67.88,'2024-07-03'),(2,'26442RAD3','WFS',5600,78.56,'2024-07-03'),(3,'459200GJ4','WFS',65000,91.10,'2024-07-03'),(4,'929903DT6','WFS',5000,79.90,'2024-07-03'),(5,'931142DH3','WFS',5000,69.90,'2024-07-03'),(6,'02079KAC1','WFS',3400,67.88,'2024-07-03'),(7,'14149YAZ1','WFS',4500,67.88,'2024-07-03'),(8,'931142DH3','WFS',4500,67.88,'2024-07-03'),(9,'59156RBB3','JPMC',6000,65.00,'2024-07-03'),(10,'50076QAZ9','JPMC',6000,89.00,'2024-07-03'),(11,'20030NBP5','GC',4500,67.00,'2024-07-03'),(12,'459200GJ4','GC',4500,78.00,'2024-07-02'),(13,'14149YAZ1','BOA',4500,78.00,'2024-07-02'),(14,'172967FT3','BLACKROCK',5600000,79.98,'2024-07-02'),(15,'931142DH3','SSNC',5677000,66.89,'2024-07-02'),(16,'49326EE99','BOA',3456660,67.88,'2024-07-02'),(17,'084670BR9','NYB',4455500,78.99,'2024-07-02'),(18,'478160BV5','FIDELITY',560000,77.12,'2024-07-02'),(31,'931142DH4','JPMC',56777,78.00,'2024-07-03'),(32,'172967FT4','ABERDEEN',56890,89.00,'2024-07-03'),(33,'084670BR8','GC',67890,69.00,'2024-07-03');
Create VIEW `top5tradedbonds` AS select `trace`.`CUSIP` AS `cusip`,sum(`trace`.`QUANTITY`) AS `quantity` from `trace` group by `trace`.`CUSIP` order by `quantity` desc limit 5 ;

-- what are the top 5 traded bonds today
select cusip, sum(quantity) as quantity from trace group by cusip order by quantity desc limit 5;

-- Which bonds out of the top traded bonds today did we miss
select s.cusip, s.ticker from security s inner join trace t on t.cusip = s.cusip where dealer <>'WFS' 
AND s.CUSIP NOT IN (select cusip from trades);


-- by what margin did we miss the top traded bonds today?
select t1.cusip, s.ticker,( t1.price - t2.price) as margin, t2.dealer from trades t1 
inner join security s on t1.cusip = s.cusip
left join trace t2 on t2.cusip = s.cusip
where t2.dealer <> 'WFS' and s.cusip in (select cusip from top5tradedbonds) order by margin desc;

-- Can you tell me if we have any LIVE offerings on them at all?
select t1.cusip, s.ticker, o.quantity, o.active from trades t1 
inner join security s on t1.cusip = s.cusip
left join trace t2 on t2.cusip = s.cusip
inner join offers o on o.cusip = s.cusip
where t2.dealer <> 'WFS' and active = 1 and s.cusip in (select cusip from top5tradedbonds);

-- Hey Lumen: compare the supply with current demand on these top traded tickers?
select s.cusip, s.ticker, o.quantity as supply, t.quantity as demand, o.active from security s 
inner join offers o on s.cusip = o.cusip
inner join trace t on t.cusip = s.cusip
where active = 1;

-- Can you show this in a different way
