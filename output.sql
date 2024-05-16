CREATE TABLE `stockmarket` (
  `ID` int NOT NULL, -- unique id
  `StockName` varchar(100) DEFAULT NULL, -- name of the stock
  `StockSymbol` varchar(10) DEFAULT NULL, -- symbol of the stock
  `MarketCap` bigint DEFAULT NULL, -- marketcap of the stock
  `Price` decimal(10,2) DEFAULT NULL, -- price of the stock
  `Volume` bigint DEFAULT NULL, -- volume of the stock
  `Changes` decimal(10,2) DEFAULT NULL, -- stock price changes, can be called as change too
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

