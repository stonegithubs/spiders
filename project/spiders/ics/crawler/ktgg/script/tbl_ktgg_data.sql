
SET NAMES utf8mb4;


DROP TABLE IF EXISTS `tbl_ktgg_data`;

CREATE TABLE `tbl_ktgg_data` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `ename` VARCHAR(128) NOT NULL COMMENT '爬虫名称/英文',
    `cname` VARCHAR(128) NOT NULL COMMENT '开庭公告名称/中文名',
    `unique_id` CHAR(32) NOT NULL COMMENT '唯一标识',
    `title` VARCHAR(128) DEFAULT NULL COMMENT '标题',
    `body` text DEFAULT NULL COMMENT '正文',
    `court` varchar(64) DEFAULT NULL COMMENT '法院',
    `court_room` varchar(64) DEFAULT NULL COMMENT '法庭名称',
    `court_date` varchar(32) DEFAULT NULL COMMENT '开庭日期',
    `case_number` varchar(128) DEFAULT NULL COMMENT '案号',
    `case_cause` varchar(256) DEFAULT NULL COMMENT '案由',
    `undertake_dept` varchar(64) DEFAULT NULL COMMENT '承办部门',
    `responsible_court` varchar(64) DEFAULT NULL COMMENT '承办法院',
    `presiding_judge` varchar(64) DEFAULT NULL COMMENT '主审',
    `chief_judge` varchar(128) DEFAULT NULL COMMENT '审判长',
    `judiciary` varchar(256) DEFAULT NULL COMMENT '审判员',
    `prosecutor` varchar(256) DEFAULT NULL COMMENT '原告',
    `defendant` varchar(256) DEFAULT NULL COMMENT '被告',
    `party` varchar(256) DEFAULT NULL COMMENT '当事人',
    `undertake_person` varchar(256) DEFAULT NULL COMMENT '承办人/承办法官',
    `court_member` varchar(256) DEFAULT NULL COMMENT '合议庭/合议庭成员',
    `court_clerk` varchar(256) DEFAULT NULL COMMENT '书记员',
    `case_introduction` text DEFAULT NULL COMMENT '案情简介',
    `province` varchar(32)  DEFAULT NULL COMMENT '省份',
    `url` varchar(512)  NOT NULL COMMENT '公告URl',
    `raw_id` CHAR(32) NOT NULL COMMENT '原文id',
    `domain` VARCHAR(128) NOT NULL COMMENT '域名',
    `created_at` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
	  PRIMARY KEY (`id`),
	  UNIQUE INDEX `unique_id_unique`(`unique_id`) USING BTREE,
	  INDEX `idx_ename`(`ename`) USING BTREE,
	  INDEX `idx_cname`(`cname`) USING BTREE,
    INDEX `idx_domain`(`domain`) USING BTREE,
    INDEX `idx_url`(`url`) USING BTREE,
    INDEX `idx_raw_id`(`raw_id`) USING BTREE
)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
