-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: attendance-system-python
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `picture` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Israel','Dairo','shecktardev@gmail.com','$2b$12$453/6WE/ey4sj8jqeFIb6enFPJULEeTY6fdKH12fnewud8b583qzS','','admin'),(2,'ISRAEL','EWEDAIRO','shecktarayo@gmail.com','$2b$12$nMVYgUkksSjfWCAjl7Do6e49Bg90LmCNh5Msv3HHOiSad2YUBKrbK','shecktar.jpg','user'),(3,'ayo shecktar',NULL,'iamshecktar1996@gmail.com','$2b$12$BvhRoFDiGu/HgGife39bEOZTzUEQqbKCGgWJ4Ukplp5pCCMkFZ7jW',NULL,NULL),(4,'ayo ',NULL,'mustaphaoluwatoyin2@gmail.com','$2b$12$LprV8KvHB75ddh8uT/1KdOnZAbLq2.dt/0emFtvnXrRyVcGMpSYPe',NULL,NULL),(5,'ISRAEL EWEDAIRO',NULL,'wallet95@gmail.com','$2b$12$rITBCPaGYL3jYiwtgnYwa.9fNqV8MF9is8R9hzNydeSHZvanEE8LK',NULL,NULL),(6,'OLUWATOYIN SERIFATU MUSTAPHA',NULL,'mailemmydee@gmail.com','$2b$12$hRAh5DW6.RGlnMKqG9e7DOLWCHNRc63DGG1WCxev/r8QVBv.QUqvW',NULL,NULL),(7,'OLUWATOYIN','MUSTAPHA','mustaphaoluwatoyin2@gmail.com','mustapha1211','Toyin.jpg','user'),(8,'emma','jones','shecktardev@gmail.com','abolanle12','','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-08 18:53:14
