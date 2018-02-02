CREATE TABLE `todo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `createdBy` int(11) unsigned NOT NULL,
  `dueDate` timestamp NULL DEFAULT NULL,
  `createdAt` timestamp NULL DEFAULT NULL,
  `text` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`,`createdBy`),
  KEY `createdBy` (`createdBy`),
  CONSTRAINT `todo_ibfk_1` FOREIGN KEY (`createdBy`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;