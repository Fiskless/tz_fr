-- MariaDB dump 10.19  Distrib 10.6.3-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: phone_book
-- ------------------------------------------------------
-- Server version	10.6.3-MariaDB-1:10.6.3+maria~focal

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `phone_book`
--

DROP TABLE IF EXISTS `phone_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phone_book` (
  `name` varchar(50) NOT NULL,
  `phone` varchar(12) DEFAULT NULL,
  `birthday_date` date DEFAULT NULL,
  UNIQUE KEY `phone_book_unique` (`name`,`phone`,`birthday_date`),
  UNIQUE KEY `phone_unique` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phone_book`
--

LOCK TABLES `phone_book` WRITE;
/*!40000 ALTER TABLE `phone_book` DISABLE KEYS */;
INSERT INTO `phone_book` VALUES ('Александр Сергеевич','+78542569856','1996-01-01'),('Андрей Владимирович','+79568541258','1990-07-15'),('Борис Евгеньевич','+79854632698','1999-05-13'),('Григорий','+78965412569','2000-01-01'),('Григорий Сергеевич','+78965412589','2000-01-01'),('Денис Викторович','+79856541256','1995-06-01'),('Дмитрий Викторович','+78566541269','1998-05-29'),('Егор Владимирович','+79566541258','1997-02-13'),('Константин Викторович','+79896541256','2000-01-01'),('Олег Геннадьевич','+78569856545','2000-01-01'),('Олег Сергеевич','+79856541258','2000-01-01'),('Павел Владимирович','+7985412569','2000-01-01'),('Тимофей Игоревич','+79854622656','2000-01-01');
/*!40000 ALTER TABLE `phone_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `birthday_date` date DEFAULT NULL,
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('123','123','2000-01-01'),('admin','admin',NULL),('Администратор','admin','2000-01-01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-02  0:38:09
