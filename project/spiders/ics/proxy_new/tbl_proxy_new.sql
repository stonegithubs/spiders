CREATE TABLE `tbl_proxy_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) DEFAULT NULL,
  `port` varchar(255) DEFAULT NULL,
  `expire_time` datetime DEFAULT NULL,
  `used_count` int(11) DEFAULT '0',
  `zgcpws` varchar(255) DEFAULT NULL,
  `zgcpws_grey` datetime DEFAULT NULL,
  `zgcpws_app` varchar(255) DEFAULT NULL,
  `zgcpws_app_grey` datetime DEFAULT NULL,
  `zhixing` varchar(255) DEFAULT NULL,
  `zhixing_grey` datetime DEFAULT NULL,
  `fysx` varchar(255) DEFAULT NULL,
  `fysx_grey` datetime DEFAULT NULL,
  `gsxt` varchar(255) DEFAULT NULL,
  `gsxt_grey` datetime DEFAULT NULL,
  `other` varchar(255) DEFAULT NULL,
  `other_grey` datetime DEFAULT NULL,
  `last_use_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55513 DEFAULT CHARSET=utf8;

