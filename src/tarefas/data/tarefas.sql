DROP DATABASE IF

CREATE DATABASE IF NOT EXISTS `tarefas`;

USE `tarefas`;

DROP TABLE IF EXISTS `tarefas`;

CREATE TABLE IF NOT EXISTS `tarefa` (
    `id_tarefa` INT NOT NULL PRIMARY KEY,
    `titulo_tarefa` VARCHAR(100) NOT NULL,
    `data_conclus` DATETIME NULL
);