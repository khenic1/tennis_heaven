SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema eCommerce_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema eCommerce_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `eCommerce_db` DEFAULT CHARACTER SET utf8 ;
USE `eCommerce_db` ;

-- -----------------------------------------------------
-- Table `eCommerce_db`.`admins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`admins` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`customers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`shipping_address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`shipping_address` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(45) NULL,
  `address_2` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `zip_code` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`billing_address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`billing_address` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(45) NULL,
  `address_2` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `zip_code` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`payment` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `card` INT NULL,
  `security_code` INT NULL,
  `expiration` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `order_total` VARCHAR(45) NULL,
  `shipping_address_id` INT NOT NULL,
  `billing_address_id` INT NOT NULL,
  `payment_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_customer_idx` (`customer_id` ASC),
  INDEX `fk_orders_shipping_address1_idx` (`shipping_address_id` ASC),
  INDEX `fk_orders_billing_address1_idx` (`billing_address_id` ASC),
  INDEX `fk_orders_payment1_idx` (`payment_id` ASC),
  CONSTRAINT `fk_orders_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `eCommerce_db`.`customers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_shipping_address1`
    FOREIGN KEY (`shipping_address_id`)
    REFERENCES `eCommerce_db`.`shipping_address` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_billing_address1`
    FOREIGN KEY (`billing_address_id`)
    REFERENCES `eCommerce_db`.`billing_address` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_payment1`
    FOREIGN KEY (`payment_id`)
    REFERENCES `eCommerce_db`.`payment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `inventory_count` INT NULL,
  `quantity_sold` INT NULL,
  `product_image` VARCHAR(255) NULL,
  `price` VARCHAR(45) NULL,
  `categories_id` INT NOT NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_products_categories1_idx` (`categories_id` ASC),
  CONSTRAINT `fk_products_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `eCommerce_db`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eCommerce_db`.`products_orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eCommerce_db`.`products_orders` (
  `products_id` INT NOT NULL,
  `orders_id` INT NOT NULL,
  PRIMARY KEY (`products_id`, `orders_id`),
  INDEX `fk_products_has_orders_orders1_idx` (`orders_id` ASC),
  INDEX `fk_products_has_orders_products1_idx` (`products_id` ASC),
  CONSTRAINT `fk_products_has_orders_products1`
    FOREIGN KEY (`products_id`)
    REFERENCES `eCommerce_db`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_products_has_orders_orders1`
    FOREIGN KEY (`orders_id`)
    REFERENCES `eCommerce_db`.`orders` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
