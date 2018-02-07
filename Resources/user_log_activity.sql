CREATE TABLE `user_log_activity` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `userID` int(11) unsigned NOT NULL,
  `activityType` varchar(52) DEFAULT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `ipAddress` varchar(32) DEFAULT NULL,
  `details` text,
  PRIMARY KEY (`id`,`userID`),
  KEY `userID` (`userID`),
  CONSTRAINT `user_log_activity_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;