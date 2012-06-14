-- MySQL dump 10.13  Distrib 5.1.58, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: proxyvpn
-- ------------------------------------------------------
-- Server version	5.1.58

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `squid_servers`
--

DROP TABLE IF EXISTS `squid_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `squid_servers` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ServerName` varchar(64) NOT NULL,
  `MySQL_user` varchar(64) NOT NULL,
  `MySQL_password` varchar(64) NOT NULL,
  `Comment` varchar(100) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `squid_servers`
--

LOCK TABLES `squid_servers` WRITE;
/*!40000 ALTER TABLE `squid_servers` DISABLE KEYS */;
INSERT INTO `squid_servers` VALUES (1,'localhost','proxy_usr','KDsj892ehjss','');
/*!40000 ALTER TABLE `squid_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `squid_traffic`
--

DROP TABLE IF EXISTS `squid_traffic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `squid_traffic` (
  `user` varchar(32) NOT NULL,
  `serverid` int(11) NOT NULL,
  `band_used` bigint(32) NOT NULL,
  `band_max` bigint(32) NOT NULL,
  `allow_overuse` tinyint(1) NOT NULL,
  PRIMARY KEY (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `squid_traffic`
--

LOCK TABLES `squid_traffic` WRITE;
/*!40000 ALTER TABLE `squid_traffic` DISABLE KEYS */;
INSERT INTO `squid_traffic` VALUES ('testuser',1,66638834586,0,0),('testuser2',1,0,52428800,0);
/*!40000 ALTER TABLE `squid_traffic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `squidpasswd`
--

DROP TABLE IF EXISTS `squidpasswd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `squidpasswd` (
  `user` varchar(32) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL DEFAULT '',
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `fullname` varchar(60) DEFAULT NULL,
  `comment` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `squidpasswd`
--

LOCK TABLES `squidpasswd` WRITE;
/*!40000 ALTER TABLE `squidpasswd` DISABLE KEYS */;
INSERT INTO `squidpasswd` VALUES ('testuser','098f6bcd4621d373cade4e832627b4f6',1,'Test User','for testing purpose');
/*!40000 ALTER TABLE `squidpasswd` ENABLE KEYS */;
UNLOCK TABLES;
