
SET NAMES utf8mb4;

DROP TABLE IF EXISTS `tbl_ktgg_raw`;
CREATE TABLE `tbl_ktgg_raw`  (
    `id` int(11) NOT NULL AUTO_INCREMENT,
	  `crawl_date` DATE NOT NULL COMMENT '抓取日期，年月日',
    `ename` VARCHAR(128) NOT NULL COMMENT '爬虫名/英文',
    `cname` VARCHAR(128) NOT NULL COMMENT '爬虫名称/中文',
    `raw` text NOT NULL COMMENT '原文内容',
    `raw_id` CHAR(32) NOT NULL COMMENT '原文MD5值',
    `created_at` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间年月日时分秒',
    PRIMARY KEY (`id`),
    UNIQUE INDEX `raw_id_unique`(`raw_id`) USING BTREE,
    INDEX `idx_crawl_date`(`crawl_date`) USING BTREE,
    INDEX `idx_ename`(`ename`) USING BTREE
)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
