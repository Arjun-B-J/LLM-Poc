use creditcardV2;
CREATE TABLE `customer` (
  `ACCNO` varchar(10) NOT NULL,
  `NAME` varchar(45) DEFAULT NULL,
  `CITY` varchar(45) DEFAULT NULL,
  `OUTSTANDING` varchar(45) DEFAULT NULL,
  `CREDITLINE` decimal(10,2) DEFAULT NULL,
  `COLLATERAL` int DEFAULT NULL,
  `LASTPAYMENT` datetime DEFAULT NULL,
  `BROKENPROMISES` int DEFAULT NULL,
  `LASTCONTACT` datetime DEFAULT NULL,
  `ADJUSTLIMIT` int DEFAULT NULL,
  `PartialPayments` int DEFAULT NULL,
  PRIMARY KEY (`ACCNO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `customer` VALUES ('101','Bernard','Kansas','34500',36000.00,1,'2023-07-03 00:00:00',6,'2024-07-03 00:00:00',0,NULL),('102','John','Dallas','34500',36000.00,1,'2024-03-03 00:00:00',8,'2024-07-03 00:00:00',1,1200),('103','Sachin','NY','34500',36000.00,1,'2024-04-03 00:00:00',9,'2024-07-03 00:00:00',1,NULL),('104','Lucy','Baltimore','34500',36000.00,1,'2024-03-03 00:00:00',7,'2024-07-03 00:00:00',2,2000),('105','Sonia','Newark','34500',36000.00,1,'2024-07-03 00:00:00',3,'2024-07-03 00:00:00',1,NULL),('106','Bell','Philli','34500',36000.00,1,'2024-07-03 00:00:00',2,'2024-07-03 00:00:00',1,NULL),('107','Andrew','Texas','34500',36000.00,1,'2024-07-03 00:00:00',3,'2024-07-03 00:00:00',2,NULL),('108','Grant','Atlantic City','34500',36000.00,1,'2024-07-03 00:00:00',2,'2024-07-03 00:00:00',2,NULL),('109','Rajdeep','Kansas','10000',36000.00,1,'2024-07-03 00:00:00',3,'2024-07-03 00:00:00',1,NULL),('110','Martin','Baltimore','23000',36000.00,1,'2024-02-03 00:00:00',2,'2024-07-03 00:00:00',1,2500),('111','Michael','Baltimore','23111',36000.00,1,'2024-02-03 00:00:00',6,'2024-07-03 00:00:00',1,2000),('112','Venkat','Baltimore','23500',36000.00,1,'2024-02-03 00:00:00',8,'2024-07-03 00:00:00',1,NULL),('113','Justin','Baltimore','11222',20000.00,1,'2024-02-03 00:00:00',6,'2024-07-03 00:00:00',1,NULL),('114','Kevin','Baltimore','22111',20000.00,1,'2024-02-03 00:00:00',1,'2024-07-03 00:00:00',1,NULL),('115','Anthony','Dallas','34888',34500.00,1,'2024-03-03 00:00:00',6,'2024-07-03 00:00:00',1,1800);
INSERT INTO `customer` VALUES 
('116','Alice','Houston','40000',38000.00,1,'2024-03-03 00:00:00',7,'2024-07-03 00:00:00',1,1000),
('117','Bob','San Francisco','45000',39000.00,1,'2024-02-03 00:00:00',8,'2024-07-03 00:00:00',1,2000),
('118','Charlie','Seattle','50000',40000.00,1,'2024-01-03 00:00:00',9,'2024-07-03 00:00:00',1,1500);


-- Show me the trend of customers by city who entered final delinquency today or nearing charge-off
SELECT city,
       Count(*) AS Count
FROM   customer
WHERE  Timestampdiff(day, lastpayment, Curdate()) >= 99
       AND brokenpromises > 5
GROUP  BY city; 

-- How many of them agreed on credit line adjustment or payment re-structuring along with their dues, show by city
SELECT city,
       Count(*)         AS customers,
       Sum(outstanding) AS dues
FROM   customer
WHERE  Timestampdiff(day, lastpayment, Curdate()) >= 99
       AND brokenpromises > 5
       AND adjustlimit > 0
GROUP  BY city; 
-- Provide more details around these customers and include their collateral status
SELECT accno,
       NAME,
       city,
       outstanding,
       creditline,
       collateral,
       lastpayment,
       brokenpromises,
       lastcontact,
       adjustlimit,
       partialpayments
FROM   customer
WHERE  Timestampdiff(day, lastpayment, Curdate()) >= 99
       AND brokenpromises > 5
       AND adjustlimit > 0; 



