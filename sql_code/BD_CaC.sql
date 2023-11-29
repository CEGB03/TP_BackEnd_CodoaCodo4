-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS `bd_cac_fsp`;

-- Usar la base de datos
USE `bd_cac_fsp`;

CREATE TABLE `clientes` (
    `idCliente` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(50) NOT NULL,
    `idCompra` INT NOT NULL,
    PRIMARY KEY (`idCliente`)
)  ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_0900_AI_CI;

-- Definir la tabla conciertos
/*DROP TABLE IF EXISTS `conciertos`;*/
CREATE TABLE `conciertos` (
  `idConciertos` int NOT NULL AUTO_INCREMENT,
  `concierto` varchar(255) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `precio` int NOT NULL,
  PRIMARY KEY (`idConciertos`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Definir la tabla compra
/*DROP TABLE IF EXISTS `compra`;*/
CREATE TABLE `compra` (
  `idCompra` int NOT NULL AUTO_INCREMENT,
  `numero` int NOT NULL,
  `fecha` datetime NOT NULL,
  `cantCompra` int NOT NULL,
  `idCliente` int NOT NULL,
  `idConcierto` int NOT NULL,
  PRIMARY KEY (`idCompra`),
  KEY `idCliente` (`idCliente`),
  KEY `idConcierto` (`idConcierto`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `clientes` (`idCliente`),
  CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`idConcierto`) REFERENCES `conciertos` (`idConciertos`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `clientes` (`idCliente`, `nombre`, 	 	 `idCompra`) VALUES
							(1, 	'Juan Pérez', 	 	 2),
							(2, 	 'Ana Gómez', 	 	 3),
							(3, 	 'Carlos López', 	 1);

INSERT INTO `conciertos` (`idConciertos`, `concierto`,  	`cantidad`, `precio`) VALUES
							(1, 	 	 'Luis Miguel', 	 100, 	 	 30),
							(2, 	 	 'Paul McCartney',   50, 	 	 60),
							(3, 	 	 'Callejero Fino', 	 50, 	 	 25),
							(4, 	 	 'Tini Stoesel', 	 40, 	 	 35),
							(5, 	 	 'LGante', 	 	 	 50, 	 	 60),
							(6, 	 	 'Mona Jimenez', 	 80, 	 	 25);

-- Insertar datos de prueba para la tabla compra
INSERT INTO `compra` (`numero`, 	 `fecha`, 	 	 `idCliente`, `idConcierto`, `cantCompra`) VALUES
						(101, '2023-11-28 12:00:00', 	 3, 	 	 1, 	 	 	 5),
						(102, '2023-11-28 14:30:00',  	 1, 	 	 3, 	 	 	 3),
						(103, '2023-11-28 16:45:00', 	 2, 	 	 5, 	 	 	 2);