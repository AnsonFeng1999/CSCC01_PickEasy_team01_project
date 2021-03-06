CREATE TABLE IF NOT EXISTS `restaurant` (
  `rid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `name`         varchar(128)      NOT NULL DEFAULT '',
  `address`      varchar(256)      NOT NULL DEFAULT '',
  `uid`          int               NOT NULL,
  PRIMARY KEY (`rid`)
);
CREATE TABLE IF NOT EXISTS `user` (
  `uid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `name`         varchar(64)       NOT NULL DEFAULT '',
  `email`        varchar(128)      NOT NULL DEFAULT '',
  `password`     varchar(64)       NOT NULL DEFAULT '',
  `type`         int               NOT NULL,
  PRIMARY KEY (`uid`)
);
CREATE TABLE IF NOT EXISTS `coupons` (
  `cid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `rid`          int               NOT NULL,
  `name`         varchar(128)      NOT NULL DEFAULT '',
  `points`       int unsigned      NOT NULL,
  `description`  varchar(1028)     NOT NULL DEFAULT '',
  `level`        int unsigned      NOT NULL,
  `begin`        date,
  `expiration`   date,
  `deleted`      int               NOT NULL,
  PRIMARY KEY (`cid`)
);
CREATE TABLE IF NOT EXISTS `points` (
  `pid`          int               NOT NULL AUTO_INCREMENT,
  `uid`          int               NOT NULL,
  `rid`          int               NOT NULL,
  `points`       int               NOT NULL,
  PRIMARY KEY (`pid`)
);
CREATE TABLE IF NOT EXISTS `employee` (
  `uid`          int               NOT NULL,
  `rid`          int               NOT NULL,
  PRIMARY KEY (`uid`)
);
CREATE TABLE IF NOT EXISTS `achievements` (
  `aid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `rid`          int unsigned      NOT NULL,
  `name`         varchar(128)      NOT NULL DEFAULT '',
  `experience`   int unsigned      NOT NULL,
  `points`       int unsigned      NOT NULL,
  `type`         int unsigned,
  `value`        varchar(2048)     NOT NULL DEFAULT '',
  PRIMARY KEY (`aid`)
);
CREATE TABLE IF NOT EXISTS `redeemed_coupons` (
  `rcid`         int               NOT NULL AUTO_INCREMENT,
  `cid`          int unsigned      NOT NULL,
  `rid`          int unsigned      NOT NULL,
  `uid`          int unsigned      NOT NULL,
  `valid`        int unsigned      NOT NULL,
  PRIMARY KEY (`rcid`)
);
CREATE TABLE IF NOT EXISTS `customer_achievement_progress` (
  `aid`          int unsigned      NOT NULL,
  `uid`          int unsigned      NOT NULL,
  `progress`     int unsigned      NOT NULL,
  `total`        int unsigned      NOT NULL,
  `update`       DATETIME          NOT NULL,
  PRIMARY KEY (`aid`, `uid`)
);
CREATE TABLE IF NOT EXISTS `experience` (
  `uid`          int               NOT NULL,
  `rid`          int               NOT NULL,
  `experience`   int               NOT NULL,
  PRIMARY KEY (`uid`, `rid`)
);
CREATE TABLE IF NOT EXISTS `thresholds` (
  `rid`          int unsigned      NOT NULL,
  `level`        int unsigned      NOT NULL,
  `reward`       int unsigned      NOT NULL,
  PRIMARY KEY (`rid`, `level`)
);
CREATE TABLE IF NOT EXISTS `favourite` (
  `uid`          int unsigned      NOT NULL,
  `rid`          int unsigned      NOT NULL,
  PRIMARY KEY (`uid`, `rid`)
);
