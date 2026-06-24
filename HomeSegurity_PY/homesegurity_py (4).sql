-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-06-2026 a las 07:19:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `homesegurity_py`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agente_inmobiliario`
--

CREATE TABLE `agente_inmobiliario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `especialidad` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asesoramiento`
--

CREATE TABLE `asesoramiento` (
  `id_asesoramiento` bigint(20) NOT NULL,
  `id_agente_inmobiliario` int(11) DEFAULT NULL,
  `id_citas` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avaluo`
--

CREATE TABLE `avaluo` (
  `id_avaluo` bigint(20) NOT NULL,
  `id_vivienda` bigint(20) NOT NULL,
  `id_usuario` bigint(20) NOT NULL,
  `id_perito` bigint(20) DEFAULT NULL,
  `area_m2` decimal(10,2) NOT NULL,
  `localidad` varchar(100) NOT NULL,
  `precio_m2` decimal(12,2) NOT NULL,
  `valor_total` decimal(15,2) NOT NULL,
  `antiguedad` int(11) DEFAULT NULL,
  `estrato` int(11) DEFAULT NULL,
  `parqueadero` tinyint(1) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `solicitante` varchar(100) DEFAULT 'Sin nombre',
  `correo` varchar(100) DEFAULT 'sin_correo@mail.com'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `avaluo`
--

INSERT INTO `avaluo` (`id_avaluo`, `id_vivienda`, `id_usuario`, `id_perito`, `area_m2`, `localidad`, `precio_m2`, `valor_total`, `antiguedad`, `estrato`, `parqueadero`, `descripcion`, `fecha`, `solicitante`, `correo`) VALUES
(2, 5, 1, NULL, 45.00, 'Suba', 5200000.00, 231660000.00, 2, 3, 0, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Suba, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 06:56:26', '', ''),
(3, 4, 4, 1, 52.00, 'Engativá', 4000000.00, 220920000.00, 2, 3, 1, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Engativá, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 07:07:14', '', ''),
(4, 4, 21, NULL, 52.00, 'Engativá', 4000000.00, 220920000.00, 2, 3, 1, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Engativá, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 07:28:06', '', ''),
(5, 5, 4, 1, 45.00, 'Suba', 5200000.00, 231660000.00, 2, 3, 0, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Suba, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 07:51:47', 'jose rincon', 'joserinconxc2008@gmail.com'),
(19, 4, 23, 1, 54.00, 'engativa', 40000.00, 2160000.00, 2, 4, NULL, 'bonita', '2026-04-08 09:46:33', 'Jose gabriel gutierrez rincon', 'joserinconxc2008@gmail.com'),
(20, 4, 24, 1, 52.00, 'Engativá', 4000000.00, 220920000.00, 2, 3, 1, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Engativá, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 17:15:06', 'adres cepeda', 'joserinconxc2008@gmail.com'),
(21, 4, 21, 1, 52.00, 'Engativá', 4000000.00, 220920000.00, 2, 3, 1, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Engativá, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 17:23:40', 'jose rincon', 'joserinconxc2008@gmail.com'),
(22, 5, 25, NULL, 45.00, 'Suba', 5200000.00, 231660000.00, 2, 3, 0, '\nEl valor fue calculado según el precio promedio del metro cuadrado\nen Suba, ajustado por estrato socioeconómico,\nantigüedad del inmueble y características adicionales.\n', '2026-04-08 18:24:27', 'Santiago ramirez', 'joserinconxc2007@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avaluos`
--

CREATE TABLE `avaluos` (
  `id` bigint(20) NOT NULL,
  `tipo_inmueble` varchar(50) NOT NULL,
  `modalidad` varchar(50) NOT NULL,
  `valorEstimado` double DEFAULT NULL,
  `areaTerreno` double DEFAULT NULL,
  `areaConstruccion` double DEFAULT NULL,
  `antiguedad` int(11) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `caracteristicaSector` varchar(255) DEFAULT NULL,
  `localizacion` varchar(255) DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `barrio` varchar(100) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT 'Bogotá D.C.',
  `solicitante` varchar(100) DEFAULT NULL,
  `fechaVisita` date DEFAULT NULL,
  `imagenes` text DEFAULT NULL,
  `cliente_id` bigint(20) DEFAULT NULL,
  `perito_id` bigint(20) DEFAULT NULL,
  `habitaciones` int(11) DEFAULT 0,
  `banos` int(11) DEFAULT 0,
  `parqueaderos` int(11) DEFAULT 0,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cita`
--

CREATE TABLE `cita` (
  `id_cita` bigint(20) NOT NULL,
  `idUsuario` bigint(20) NOT NULL,
  `id_vivienda` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `estado` enum('PENDIENTE','APROBADA','CANCELADA') DEFAULT 'PENDIENTE',
  `recomendaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id` bigint(20) NOT NULL,
  `vivienda_id` bigint(20) DEFAULT NULL,
  `id_usuario_fk` bigint(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'PENDIENTE',
  `recomendaciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id`, `vivienda_id`, `id_usuario_fk`, `fecha`, `hora`, `estado`, `recomendaciones`) VALUES
(5, 4, 21, '2026-04-10', '02:03:00', 'PENDIENTE', NULL),
(6, 4, 4, '2026-04-10', '17:38:00', 'Aprobada', 'La cita ha sido confirmada. Por favor, asistir puntualmente con identificación.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` bigint(20) NOT NULL,
  `idUsuario` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `idUsuario`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 20),
(7, 23),
(8, 24),
(9, 25),
(10, 27),
(11, 28);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favorito`
--

CREATE TABLE `favorito` (
  `id` bigint(20) NOT NULL,
  `vivienda_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inmuebles`
--

CREATE TABLE `inmuebles` (
  `id` bigint(20) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `precio` double DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id` bigint(20) NOT NULL,
  `id_usuario` bigint(20) DEFAULT NULL,
  `id_vivienda` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perito`
--

CREATE TABLE `perito` (
  `id_perito` bigint(20) NOT NULL,
  `idUsuario` bigint(20) NOT NULL,
  `registro_raa` varchar(100) NOT NULL,
  `categoria_especializacion` varchar(100) NOT NULL,
  `formacion_academica` varchar(150) NOT NULL,
  `experiencia_anios` varchar(2) NOT NULL,
  `direccion_oficina` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perito`
--

INSERT INTO `perito` (`id_perito`, `idUsuario`, `registro_raa`, `categoria_especializacion`, `formacion_academica`, `experiencia_anios`, `direccion_oficina`) VALUES
(1, 21, 'PENDIENTE', 'Vivienda Urbana', 'Profesional', '0', 'calle 83#103c- 55');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitudes_admin`
--

CREATE TABLE `solicitudes_admin` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) DEFAULT 'PENDIENTE',
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `cargo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitudes_admin`
--

INSERT INTO `solicitudes_admin` (`id`, `usuario_id`, `correo`, `fecha`, `estado`, `nombre`, `apellido`, `cargo`) VALUES
(11, NULL, 'joserinconxc2008@gmail.com', '2026-04-07 08:59:08', 'APROBADO', 'jose', 'rincon', 'PERITO'),
(12, NULL, 'joserinconxc2008@gmail.com', '2026-04-08 04:55:29', 'PENDIENTE', 'jose', 'rincon', 'ADMIN'),
(13, NULL, 'joserinconxc2007@gmail.com', '2026-04-08 08:27:50', 'APROBADO', 'jose', 'rincon', 'ADMIN'),
(14, NULL, 'goofyart055@gmail.com', '2026-04-08 17:55:17', 'APROBADO', 'nicolas rodriguez', 'bermudez', 'AGENTE'),
(15, NULL, 'lgclavijosena@gmail.com', '2026-04-08 18:18:49', 'APROBADO', 'Clavijo', 'ortiz', 'ADMIN');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` bigint(20) NOT NULL,
  `primerNombre` varchar(100) DEFAULT NULL,
  `primerApellido` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) NOT NULL,
  `edad` int(11) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `num_documento` varchar(50) DEFAULT NULL,
  `correo` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `estadoCuenta` varchar(50) DEFAULT NULL,
  `rol` varchar(20) DEFAULT 'USER',
  `estado_admin` varchar(20) DEFAULT 'NO_APLICA',
  `admin_token` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `primerNombre`, `primerApellido`, `contraseña`, `edad`, `direccion`, `num_documento`, `correo`, `telefono`, `estadoCuenta`, `rol`, `estado_admin`, `admin_token`) VALUES
(1, 'nicolas', 'bermudez', 'Segura#2024!HS', 20, 'Calle 72 #45-19, Bogotá D.C., Colombia', '1010962170', 'rodriguezbermudeznicolas@gmail.com', '3113838140', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(2, 'ALIS', 'VARGAS', 'Segura#2024!HS', 19, 'alisUrbanovargas@gmial.com', '324234234', 'alisgurvano@gmail.com', '3113838140', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(3, 'luis', 'posada', 'Segura#2024!HS', 22, 'rodriguezbermudeznicolas@gmail.com', '23213123213', 'luis@gmail', '3113838140', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(4, 'jose', 'rincon', 'Joserincon2812@', 19, 'jose@gmail.com', '1014596650', 'jose@gmail.com', '3212575103', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(5, 'jose', 'rincon', 'Jose2812@', 19, 'calle 83#103c- 55', '1014596650', 'jose@admin.com', '3212575103', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(20, 'jose', 'rincon', 'Jose2812@', 22, 'calle 83#103c- 55', '1014596650', 'joserinconxc2008@homesecurity.com', '+573212575103', 'ACTIVO', 'USER', 'PENDIENTE', 'rWZX-7_SZjM4wsNNKlS-gBw0fT-FQ3WITiKaCLUmp2o'),
(21, 'jose', 'rincon', 'W5VhaBJLhg', 22, 'calle 83#103c- 55', '1014596650', 'joserinconxc2008@gmail.com', '+573212575103', 'ACTIVO', 'PERITO', 'PENDIENTE', '7902597b-dc3f-40e0-b2d7-ddb40c20697f'),
(23, 'jose', 'rincon', 'Jose2812@', 19, 'calle 83', '1014596650', 'joserinconxc2007@gmail.com', '3224737591', 'ACTIVO', 'ADMIN', 'NO_APLICA', NULL),
(24, 'adres', 'cepeda', 'Jose2812@', 22, 'calle 83#103c- 55', '1014596650', 'andres@gmail.com', '+573212575103', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(25, 'Santiago', 'ramirez', 'Jose2812@', 22, 'cra112b#77c47', '1015789942', 'santiago@gmail.com', '+573212575103', 'ACTIVO', 'USER', 'NO_APLICA', NULL),
(27, 'rodriguez', 'be', 'aqEkETu1Gx', 22, '3224737591', '1014596650', 'goofyart055@gmail.com', '+573212575103', 'ACTIVO', 'AGENTE', 'NO_APLICA', NULL),
(28, 'elena', 'clavijo', 'h4lmIznw0R', 15, 'calle 83#103c- 55', 'abcd', 'lgclavijosena@gmail.com', '1', 'ACTIVO', 'ADMIN', 'NO_APLICA', NULL);

--
-- Disparadores `usuario`
--
DELIMITER $$
CREATE TRIGGER `after_usuario_insert_cliente` AFTER INSERT ON `usuario` FOR EACH ROW BEGIN
    IF NEW.rol = 'USER' THEN
        INSERT INTO cliente (idUsuario)
        VALUES (NEW.idUsuario);
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_usuario_insert_perito` AFTER INSERT ON `usuario` FOR EACH ROW BEGIN
    IF NEW.rol = 'PERITO' THEN
        INSERT INTO perito (
            idUsuario, 
            registro_raa, 
            categoria_especializacion, 
            formacion_academica, 
            experiencia_anios, 
            direccion_oficina
        )
        VALUES (
            NEW.idUsuario, 
            'PENDIENTE', -- Valor temporal requerido por la restricción NOT NULL
            'POR DEFINIR', 
            'POR DEFINIR', 
            '0', 
            NEW.direccion -- Toma la dirección base del usuario
        );
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vivienda`
--

CREATE TABLE `vivienda` (
  `id_vivienda` bigint(20) NOT NULL,
  `id_asesoramiento` bigint(20) DEFAULT NULL,
  `id_avaluo` bigint(20) DEFAULT NULL,
  `ciudad` varchar(120) NOT NULL,
  `localidad` varchar(100) NOT NULL,
  `area_m2` decimal(10,2) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `precio` decimal(12,2) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado_publicacion` enum('ACTIVO','INACTIVO','VENDIDO') DEFAULT 'ACTIVO',
  `tipo_inmueble` enum('CASA','APARTAMENTO','LOCAL') NOT NULL,
  `estrato` int(11) NOT NULL,
  `habitaciones` int(11) DEFAULT 0,
  `banos` int(11) DEFAULT 0,
  `parqueaderos` int(11) DEFAULT 0,
  `antiguedad` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vivienda`
--

INSERT INTO `vivienda` (`id_vivienda`, `id_asesoramiento`, `id_avaluo`, `ciudad`, `localidad`, `area_m2`, `direccion`, `precio`, `descripcion`, `foto`, `fecha_registro`, `estado_publicacion`, `tipo_inmueble`, `estrato`, `habitaciones`, `banos`, `parqueaderos`, `antiguedad`) VALUES
(4, NULL, NULL, 'Bogotá D.C.', 'Engativá', 52.00, 'calle 83#103c- 55', 2000000000.00, 'hermosa cas en la localidad de engativa ', 'apartamento1.jpg', '2026-04-07 06:16:24', 'ACTIVO', 'CASA', 3, 2, 1, 1, 2),
(5, NULL, NULL, 'Bogotá D.C.', 'Suba', 45.00, 'calle 83#103c- 55', 20000000.00, '', 'apartamento1.jpg', '2026-04-08 05:33:36', 'ACTIVO', 'APARTAMENTO', 3, 4, 2, 0, 2),
(6, NULL, NULL, 'Bogotá D.C.', 'Bosa', 45.00, 'cra112b#77c47', 35000000.00, 'hermoso apartamento en la localidad de bosa con aplios espacios para tatoda la familia', 'apartamento2.jpg', '2026-04-08 17:59:24', 'ACTIVO', 'APARTAMENTO', 3, 2, 1, 0, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `agente_inmobiliario`
--
ALTER TABLE `agente_inmobiliario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `asesoramiento`
--
ALTER TABLE `asesoramiento`
  ADD PRIMARY KEY (`id_asesoramiento`),
  ADD KEY `id_agente_inmobiliario` (`id_agente_inmobiliario`),
  ADD KEY `id_citas` (`id_citas`);

--
-- Indices de la tabla `avaluo`
--
ALTER TABLE `avaluo`
  ADD PRIMARY KEY (`id_avaluo`),
  ADD KEY `fk_avaluo_vivienda` (`id_vivienda`),
  ADD KEY `fk_avaluo_usuario` (`id_usuario`),
  ADD KEY `fk_avaluo_perito` (`id_perito`);

--
-- Indices de la tabla `avaluos`
--
ALTER TABLE `avaluos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `perito_id` (`perito_id`);

--
-- Indices de la tabla `cita`
--
ALTER TABLE `cita`
  ADD PRIMARY KEY (`id_cita`),
  ADD KEY `fk_cita_usuario` (`idUsuario`),
  ADD KEY `fk_cita_vivienda` (`id_vivienda`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vivienda_id` (`vivienda_id`),
  ADD KEY `id_usuario_fk` (`id_usuario_fk`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `idUsuario` (`idUsuario`);

--
-- Indices de la tabla `favorito`
--
ALTER TABLE `favorito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vivienda_id` (`vivienda_id`);

--
-- Indices de la tabla `inmuebles`
--
ALTER TABLE `inmuebles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_vivienda` (`id_vivienda`);

--
-- Indices de la tabla `perito`
--
ALTER TABLE `perito`
  ADD PRIMARY KEY (`id_perito`),
  ADD KEY `idUsuario` (`idUsuario`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `solicitudes_admin`
--
ALTER TABLE `solicitudes_admin`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `vivienda`
--
ALTER TABLE `vivienda`
  ADD PRIMARY KEY (`id_vivienda`),
  ADD KEY `fk_asesoramiento` (`id_asesoramiento`),
  ADD KEY `fk_avaluo` (`id_avaluo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `agente_inmobiliario`
--
ALTER TABLE `agente_inmobiliario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asesoramiento`
--
ALTER TABLE `asesoramiento`
  MODIFY `id_asesoramiento` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `avaluo`
--
ALTER TABLE `avaluo`
  MODIFY `id_avaluo` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `avaluos`
--
ALTER TABLE `avaluos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cita`
--
ALTER TABLE `cita`
  MODIFY `id_cita` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `favorito`
--
ALTER TABLE `favorito`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inmuebles`
--
ALTER TABLE `inmuebles`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `perito`
--
ALTER TABLE `perito`
  MODIFY `id_perito` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `solicitudes_admin`
--
ALTER TABLE `solicitudes_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `vivienda`
--
ALTER TABLE `vivienda`
  MODIFY `id_vivienda` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asesoramiento`
--
ALTER TABLE `asesoramiento`
  ADD CONSTRAINT `asesoramiento_ibfk_1` FOREIGN KEY (`id_agente_inmobiliario`) REFERENCES `agente_inmobiliario` (`id`),
  ADD CONSTRAINT `asesoramiento_ibfk_2` FOREIGN KEY (`id_citas`) REFERENCES `citas` (`id`);

--
-- Filtros para la tabla `avaluo`
--
ALTER TABLE `avaluo`
  ADD CONSTRAINT `fk_avaluo_perito` FOREIGN KEY (`id_perito`) REFERENCES `perito` (`id_perito`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_avaluo_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_avaluo_vivienda` FOREIGN KEY (`id_vivienda`) REFERENCES `vivienda` (`id_vivienda`) ON DELETE CASCADE;

--
-- Filtros para la tabla `avaluos`
--
ALTER TABLE `avaluos`
  ADD CONSTRAINT `avaluos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `avaluos_ibfk_2` FOREIGN KEY (`perito_id`) REFERENCES `perito` (`id_perito`);

--
-- Filtros para la tabla `cita`
--
ALTER TABLE `cita`
  ADD CONSTRAINT `fk_cita_usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_cita_vivienda` FOREIGN KEY (`id_vivienda`) REFERENCES `vivienda` (`id_vivienda`) ON DELETE CASCADE;

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`vivienda_id`) REFERENCES `vivienda` (`id_vivienda`),
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`id_usuario_fk`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `favorito`
--
ALTER TABLE `favorito`
  ADD CONSTRAINT `favorito_ibfk_1` FOREIGN KEY (`vivienda_id`) REFERENCES `vivienda` (`id_vivienda`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`idUsuario`),
  ADD CONSTRAINT `pagos_ibfk_2` FOREIGN KEY (`id_vivienda`) REFERENCES `vivienda` (`id_vivienda`);

--
-- Filtros para la tabla `perito`
--
ALTER TABLE `perito`
  ADD CONSTRAINT `perito_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `vivienda`
--
ALTER TABLE `vivienda`
  ADD CONSTRAINT `fk_asesoramiento` FOREIGN KEY (`id_asesoramiento`) REFERENCES `asesoramiento` (`id_asesoramiento`),
  ADD CONSTRAINT `fk_avaluo` FOREIGN KEY (`id_avaluo`) REFERENCES `avaluos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
