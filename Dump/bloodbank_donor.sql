-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bloodbank
-- ------------------------------------------------------
-- Server version	9.0.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor` (
  `D_ID` int NOT NULL AUTO_INCREMENT,
  `DNAME` varchar(50) DEFAULT NULL,
  `SEX` varchar(10) DEFAULT NULL,
  `AGE` int DEFAULT NULL,
  `WEIGHT` int DEFAULT NULL,
  `ADDRESS` varchar(150) DEFAULT NULL,
  `DISEASE` varchar(50) DEFAULT NULL,
  `DEMAIL` varchar(100) DEFAULT NULL,
  `DONOR_DATE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `BLOODGROUP` varchar(4) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`D_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES `donor` WRITE;
/*!40000 ALTER TABLE `donor` DISABLE KEYS */;
INSERT INTO `donor` VALUES (11,'Ali','Male',23,59,'Kasur','None','03094548092','2024-07-22 03:56:16','B+'),(12,'Hamza Saleem','Male',23,62,'City Chunian Kasur','None','03049588912','2024-07-22 04:09:09','A+'),(13,'Munawar Arshad','Male',22,58,'City ch','None','','2024-07-22 08:07:26','A-'),(14,'Arshad Ali','Male',34,85,'village Nizam Pura Kasur','None','03024885960','2024-07-22 17:06:28','A-'),(15,'Shoaib Rafeeq','Male',23,74,'Village Bugri Distric Kasur','None','03264046077','2024-07-22 17:11:20','AB+'),(16,'Abdul Moiz','Male',23,52,'Kasur','None','03144268667','2024-07-22 20:16:44','AB-'),(17,'Zulqarnain','Male',23,72,'Theeng Mod Kasur','None','03000968574','2024-07-22 20:19:08','O+'),(18,'Khizar Ali','Male',24,78,'village Nizam Pura Kasur','None','03094957197','2024-07-22 20:20:58','O-'),(19,'Arslan ','Male',25,72,'village Sikandar Pura','None','03064308868','2024-07-22 20:23:25','B-');
/*!40000 ALTER TABLE `donor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-05  9:55:10
