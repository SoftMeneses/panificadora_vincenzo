-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: panificadora
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `id_insumo` int NOT NULL AUTO_INCREMENT COMMENT 'id del insumo',
  `descr` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL COMMENT 'descripcion del insumo',
  `id_und_med` int NOT NULL COMMENT 'id de la unidad de medida',
  `exist_min` smallint NOT NULL COMMENT 'existencia minima',
  `exist_max` smallint NOT NULL COMMENT 'existencia maxima',
  `stock` smallint NOT NULL COMMENT 'cantidad disponible',
  PRIMARY KEY (`id_insumo`),
  KEY `insumos_unidades_idx` (`id_und_med`),
  CONSTRAINT `insumos_unidades` FOREIGN KEY (`id_und_med`) REFERENCES `unidades` (`id_und_med`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='informacion referente a insumos utilizados';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
INSERT INTO `insumos` VALUES (1,'harina de trigo',3,10,50,25),(2,'azucar',1,20,100,48),(3,'margarina',1,10,80,30),(4,'leche',4,15,60,22),(5,'huevos',5,5,30,8),(6,'sal',1,10,20,13),(7,'levadura',1,20,50,40);
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `panes`
--

DROP TABLE IF EXISTS `panes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `panes` (
  `id_pan` int NOT NULL AUTO_INCREMENT COMMENT 'id del pan',
  `descr_pan` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL COMMENT 'descripcion del pan',
  PRIMARY KEY (`id_pan`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='informacion referente a los panes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `panes`
--

LOCK TABLES `panes` WRITE;
/*!40000 ALTER TABLE `panes` DISABLE KEYS */;
INSERT INTO `panes` VALUES (1,'campesino'),(2,'azucarado'),(3,'de leche'),(4,'de maiz'),(5,'camaleon'),(6,'de mantequilla');
/*!40000 ALTER TABLE `panes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `panes_insumos`
--

DROP TABLE IF EXISTS `panes_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `panes_insumos` (
  `id_registro` int NOT NULL AUTO_INCREMENT COMMENT 'id del registro',
  `id_pan` int NOT NULL COMMENT 'id del pan',
  `id_insumo` int NOT NULL COMMENT 'id del insumo',
  `cant_insumo` decimal(20,2) NOT NULL DEFAULT '0.00' COMMENT 'cantidad utilizada del insumo',
  `id_und_med` int NOT NULL COMMENT 'unidad de medida',
  PRIMARY KEY (`id_registro`),
  KEY `panes_insumos_panes_idx` (`id_pan`),
  KEY `panes_insumos_insumos_idx` (`id_insumo`),
  KEY `panes_insumos_unidades_idx` (`id_und_med`),
  CONSTRAINT `panes_insumos_insumos` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON UPDATE CASCADE,
  CONSTRAINT `panes_insumos_panes` FOREIGN KEY (`id_pan`) REFERENCES `panes` (`id_pan`) ON UPDATE CASCADE,
  CONSTRAINT `panes_insumos_unidades` FOREIGN KEY (`id_und_med`) REFERENCES `unidades` (`id_und_med`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='informacion referente a insumos utilizados para elaboracion de tipo de pan especifico';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `panes_insumos`
--

LOCK TABLES `panes_insumos` WRITE;
/*!40000 ALTER TABLE `panes_insumos` DISABLE KEYS */;
INSERT INTO `panes_insumos` VALUES (1,1,1,1.00,3),(2,1,6,0.50,1),(3,1,7,50.00,2),(4,2,1,1.00,3),(5,2,2,2.00,1),(6,2,4,1.00,4),(7,2,5,0.50,5),(8,3,1,1.00,3),(9,3,4,2.00,4),(10,3,7,50.00,2);
/*!40000 ALTER TABLE `panes_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades`
--

DROP TABLE IF EXISTS `unidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades` (
  `id_und_med` int NOT NULL AUTO_INCREMENT COMMENT 'id de la unidad',
  `descr_und` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL COMMENT 'descripcion de la unidad',
  PRIMARY KEY (`id_und_med`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci COMMENT='informacion referente a unidades de medida';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades`
--

LOCK TABLES `unidades` WRITE;
/*!40000 ALTER TABLE `unidades` DISABLE KEYS */;
INSERT INTO `unidades` VALUES (1,'kilo'),(2,'gramo'),(3,'saco'),(4,'litro'),(5,'carton');
/*!40000 ALTER TABLE `unidades` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-16 21:06:20
