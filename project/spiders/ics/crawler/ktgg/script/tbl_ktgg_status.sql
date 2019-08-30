/*
Navicat MySQL Data Transfer

Source Server         : 线上-微软云(ktgg)
Source Server Version : 50500
Source Host           : spider.mysqldb.chinacloudapi.cn:3306
Source Database       : spider_batch

Target Server Type    : MYSQL
Target Server Version : 50500
File Encoding         : 65001

Date: 2018-09-29 15:34:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tbl_ktgg_status
-- ----------------------------
DROP TABLE IF EXISTS `tbl_ktgg_status`;
CREATE TABLE `tbl_ktgg_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `crawl_date` date NOT NULL,
  `ename` varchar(128) NOT NULL,
  `cname` varchar(64) NOT NULL,
  `developer` varchar(64) NOT NULL,
  `state` smallint(6) NOT NULL,
  `success_cnt` int(11) DEFAULT '0',
  `duplicate_cnt` int(11) DEFAULT '0',
  `error_cnt` int(11) DEFAULT '0',
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tbl_ktgg_status_crawl_date_ename_6c4880a2_uniq` (`crawl_date`,`ename`),
  KEY `tbl_ktgg_status_ename_fc062ba7` (`ename`),
  KEY `tbl_ktgg_status_cname_4e6fd5da` (`cname`),
  KEY `tbl_ktgg_status_state_4eac0659` (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
