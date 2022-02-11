DROP TABLE IF EXISTS `panier`;
DROP TABLE IF EXISTS `ligne_commande`;
DROP TABLE IF EXISTS `commande`;
DROP TABLE IF EXISTS `meuble`; 
DROP TABLE IF EXISTS `marque`;
DROP TABLE IF EXISTS `type_meuble`;
DROP TABLE IF EXISTS `etat`;
DROP TABLE IF EXISTS `user`;


CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT AUTO_INCREMENT,
    `username` VARCHAR(255),
    `email` VARCHAR(255),
    `password` VARCHAR(255),
    `role` VARCHAR(255),
    `est_actif` TINYINT,
    `pseudo` VARCHAR(255),

    PRIMARY KEY(`user_id`) 
);


CREATE TABLE IF NOT EXISTS `etat` (
    `etat_id` INT AUTO_INCREMENT,
    `libelle` VARCHAR(10),

    PRIMARY KEY(`etat_id`)
);


CREATE TABLE IF NOT EXISTS `type_meuble` (
    `type_meuble_id` INT AUTO_INCREMENT,
    `type_meuble_libelle` VARCHAR(255),

    PRIMARY KEY(`type_meuble_id`)
);


CREATE TABLE IF NOT EXISTS `marque` (
    `marque_id` INT AUTO_INCREMENT,
    `marque_libelle` VARCHAR(255),
    
    PRIMARY KEY(`marque_id`)
);


CREATE TABLE IF NOT EXISTS `meuble` (
    `meuble_id` INT AUTO_INCREMENT,
    `nom` VARCHAR(255),
    `prix_unit` FLOAT,
    `marque_id` INT,
    `stock` INT,
    `image` VARCHAR(255),
    `type_meuble_id` INT,

    PRIMARY KEY(`meuble_id`),
    FOREIGN KEY(`marque_id`) REFERENCES `marque`(`marque_id`),
    FOREIGN KEY(`type_meuble_id`) REFERENCES `type_meuble`(`type_meuble_id`) 
);


CREATE TABLE IF NOT EXISTS `commande` (
    `commande_id` INT AUTO_INCREMENT,
    `date_achat` DATE,
    `nbr_articles` INT,
    `prix_total` FLOAT,
    `user_id` INT,
    `etat_id` INT,

    PRIMARY KEY(`commande_id`),
    FOREIGN KEY(`user_id`) REFERENCES `user`(`user_id`),
    FOREIGN KEY(`etat_id`) REFERENCES `etat`(`etat_id`)
);


CREATE TABLE IF NOT EXISTS `ligne_commande` (
    `commande_id` INT,
    `meuble_id` INT,
    `prix_unit` FLOAT,
    `quantite` INT,

    FOREIGN KEY(`commande_id`) REFERENCES `commande`(`commande_id`),
    FOREIGN KEY(`meuble_id`) REFERENCES `meuble`(`meuble_id`),
    PRIMARY KEY(`commande_id`, `meuble_id`)
);


CREATE TABLE IF NOT EXISTS `panier` (
    `panier_id` INT AUTO_INCREMENT,
    `date_ajout` DATE,
    `quantite` INT,     
    `user_id` INT,
    `meuble_id` INT,

    PRIMARY KEY(`panier_id`),
    FOREIGN KEY(`user_id`) REFERENCES `user`(`user_id`),
    FOREIGN KEY(`meuble_id`) REFERENCES `meuble`(`meuble_id`)
);


INSERT INTO `user` (`user_id`, `email`, `username`, `password`, `role`,  `est_actif`) VALUES
(NULL, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1);
INSERT INTO `user` (`user_id`, `email`, `username`, `password`, `role`, `est_actif`) VALUES
(NULL, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1);
INSERT INTO `user` (`user_id`, `email`, `username`, `password`, `role`, `est_actif`) VALUES
(NULL, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',1);

INSERT INTO `etat`(`libelle`)
VALUES('en attente'),
      ('expédié'),
      ('validé'),
      ('confirmé');

INSERT INTO `type_meuble`(`type_meuble_libelle`)
VALUES('Tables / Bureaux'),
      ('Chaises'),
      ('Ensembles'),
      ('Armoires'),
      ('Commodes'),
      ('Extérieurs');

INSERT INTO `marque` (`marque_libelle`)
VALUES('IKEA'),
      ('Mobalpa'),
      ('Maison du Monde');

INSERT INTO `meuble`(`nom`, `prix_unit`, `marque_id`, `stock`, `image`, `type_meuble_id`)
VALUES('Micke', 119.99, 3, 15, 'armoire.jpeg', 4),
      ('Citizen', 32.99, 3, 15, 'chaise.jpeg', 2),
      ('Malm', 19.99, 1, 15, 'boites.jpeg', 3),
      ('Originelle', 189.99, 2, 15, 'setTableChaises.jpg', 3),
      ('Utespelare', 124.99, 1, 15, 'table.jpeg', 1),      
      ('Brusali', 93.99, 1, 15, 'salonJardin2.jpg', 6);

-- source C:\Users\Eliot\Downloads\S2_SAE_R2.06\mysite\sql_project.sql