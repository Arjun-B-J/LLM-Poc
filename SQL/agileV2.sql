Use agileV2;
CREATE TABLE `sprints` (
  `ID` int NOT NULL,
  `TEAM` varchar(45) DEFAULT NULL,
  `GOAL` varchar(45) DEFAULT NULL,
  `POINTSCOMITTED` varchar(45) DEFAULT NULL,
  `POINTSSDELIVERED` varchar(45) DEFAULT NULL,
  `POINTSADDED` varchar(45) DEFAULT NULL,
  `INTROSPECTIVE` int DEFAULT NULL,
  `PLANNING` int DEFAULT NULL,
  `DEMO` int DEFAULT NULL,
  `WEEKLYRELEASE` int DEFAULT NULL,
  `AUTOMATION` int DEFAULT NULL,
  `SHRP` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `sprints` VALUES (1,'ALPHA','Test Prod Bugs','30','11','8',0,1,1,1,1,0),(2,'ALPHA','Upgrade to Java 17','27','13','0',0,1,0,1,1,0),(3,'ALPHA','Fix Pros issue on Position','32','9','7',1,1,1,0,0,0),(4,'HELIUM','Posiyion Changes as per Regulatory','29','12','6',1,1,1,1,1,1),(5,'HELIUM','Design the Cloud Strategy','31','11','0',0,1,0,0,0,0),(6,'HELIUM','Documet the NFR\'s E2E','34','12','1',0,0,1,0,0,0),(7,'RADON','T+1 Settlement Chages','30','12','3',1,1,1,1,1,1);

CREATE TABLE `team` (
  `ID` int NOT NULL,
  `NAME` varchar(45) DEFAULT NULL,
  `SM` varchar(45) DEFAULT NULL,
  `TMCOUNT` varchar(45) DEFAULT NULL,
  `MATURITYSCORE` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `team` VALUES (1,'ALPHA','Tim Mc Donough','6','3.1'),(2,'HELIUM','Chandan H','4','3.25'),(3,'NEON','Shalinii G','6','3.11'),(4,'ARGON','Praveen','5','2.78'),(5,'CRYPTON','Sreekanth','6','2.99'),(6,'RADON','Uday','6','2.76');
 
 
 CREATE VIEW viewavgvelocity AS 
SELECT 
    t.NAME AS name,
    AVG(s.POINTSSDELIVERED) AS velocity,
    (SUM(s.POINTSSDELIVERED) / SUM(t.TMCOUNT)) AS per_tm
FROM 
    team t 
JOIN 
    sprints s 
ON 
    t.NAME = s.TEAM
GROUP BY 
    t.NAME;
    
    
    
    
    
-- Show me the Average velocity and points per developer over the last 3 months
SELECT t.NAME,
       Round(Avg(s.pointssdelivered), 3)                  AS velocity,
       Round(Sum(s.pointssdelivered) / Sum(t.tmcount), 3) AS per_tm
FROM   team t
       INNER JOIN sprints s
               ON t.NAME = s.team
GROUP  BY t.NAME; 
    
-- How many teams are having scope creeps and by how many points on average
SELECT team,
       Count(*)         AS HowManyTimes,
       Avg(pointsadded) AS AveragePoints
FROM   sprints
WHERE  pointsadded > 0
       AND team IN (SELECT NAME
                    FROM   viewavgvelocity)
GROUP  BY team
ORDER  BY Count(*) DESC; 
-- How many times did these teams overcommit and could not complete the committed stories and by how much
SELECT team,
       Count(*)         AS HowManyTimes,
       Sum(pointsadded) AS TotalPoints
FROM   sprints
WHERE  pointsadded > 0
       AND team IN (SELECT NAME
                    FROM   viewavgvelocity)
       AND pointscomitted > pointssdelivered
GROUP  BY team
ORDER  BY Count(*) DESC; 

-- How many teams have had scope creeps on SHRP items
SELECT team,
       Count(*)         AS HowManyTimes,
       Sum(pointsadded) AS TotalPoints
FROM   sprints
WHERE  pointsadded > 0
       AND shrp > 0
       AND team IN (SELECT NAME
                    FROM   viewavgvelocity)
GROUP  BY team
ORDER  BY Count(*) DESC; 


    
    
    
 

