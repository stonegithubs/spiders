SET NAMES utf8mb4;


DROP TABLE IF EXISTS `tbl_zgcpws_increment`;

CREATE TABLE `tbl_zgcpws_increment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `do_time` datetime DEFAULT NULL COMMENT '抓取日期',
  `unpub_reason` text COMMENT '不公开理由',
  `doc_id` char(255) DEFAULT NULL COMMENT '文书ID',
  `case_name` varchar(255) DEFAULT NULL COMMENT '案件名称',
  `case_type` varchar(255) DEFAULT NULL COMMENT '案件类型',
  `case_code` varchar(255) DEFAULT NULL COMMENT '案号',
  `court` varchar(255) DEFAULT NULL COMMENT '法院名称',
  `judge_date` datetime DEFAULT NULL COMMENT '裁判日期',
  `source_text` text COMMENT '裁判要旨段原文',
  `judge_program` varchar(255) DEFAULT NULL COMMENT '审判程序',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52436 DEFAULT CHARSET=utf8;

