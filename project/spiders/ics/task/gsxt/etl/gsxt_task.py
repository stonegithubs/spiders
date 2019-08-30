#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'HeZhen'


import time
import datetime
import json
import sys
import traceback
import os
from bs4 import BeautifulSoup as bs
# import envirment vairable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(BASE_DIR)

from ics.task.gsxt.cdrcb.constant import Status
from ics.utils.db.mysql_util import MySQLUtil, CdrcbDb
from ics.utils.html import clear_noise
from ics.utils import get_ics_logger


logger = get_ics_logger(__name__)

mysql_db = CdrcbDb("cdrcb_crawl", logger)

reload(sys)
sys.setdefaultencoding('utf-8')

ETL_JSON = {}

dao = MySQLUtil("cdrcb_crawl", logger)
def error_test(source_id) :
    sql = " SELECT source_id, page_sources from gsxt_page_json\
                WHERE source_id='{}'".format(source_id)

    results = dao.query(sql)
    return results

def get_source_id():
    """
    获取所有爬取完成的source_id
    :return: resutls
    """
    # dao = MySQLInit()

    sql = " SELECT source_id, page_sources from gsxt_page_json\
            WHERE status=0 \
	        AND create_time>'2018-09-04 11:55:4'"

    results = dao.query(sql)
    return results

def update_etl_status(table_name, source_id, etl_status, id=None) :
    # dao = MySQLInit()
    sql = "update %s set etl_time='%s', etl_status=%d where source_id='%s' " % (table_name, now_time(), etl_status, source_id)
    if id:
        sql = sql + "and id={}".format(id)
    print sql
    dao.execSql(sql)

def common_query(table_name, source_id, param="") :
    # dao = MySQLInit()
    if not param:
        sql = "select page_source, id from %s where source_id='%s' and etl_status!='success'" % (table_name, source_id)
    else:
        sql = "select page_source, id, %s from %s where source_id='%s' and etl_status!='success'" % (param, table_name, source_id)
    results = dao.query(sql)
    return results

def test():
    sql = """SELECT
                    com.company_name,
                    home.page_source AS home_page_source,
                    shareholder.page_source AS shareholder_page_source,
                    keyperson.page_source as keyperson_page_source
            FROM
                gsxt_company com
             LEFT JOIN gsxt_home home ON com.company_uuid = home.company_uuid
            LEFT JOIN gsxt_shareholder shareholder ON com.company_uuid = shareholder.company_uuid
            LEFT JOIN gsxt_keyperson keyperson ON com.company_uuid = keyperson.company_uuid
            
            WHERE
                com.complete=1
            AND	home.page_source IS NOT NULL
            AND shareholder.page_source IS NOT NULL
            """

def parse_html(page_source, history_name, source_id):
    """  首页字段
         @:var social_credit_code 统一社会信用代码
         @:var company_name 企业名称
         @:var company_type 类型
         @:var legaler 法定代表人
         @:var reg_capital 注册资本 reg="register"
         @:var establish_date 成立日期
         @:var business_began 营业期限自
         @:var business_end 营业期限至
         @:var reg_ins 登记机关 reg="register" ins = "institution"
         @:var approval_date 核准日期
         @:var reg_status 登记状态 reg="register"
         @:var address 营业场所：/住所
         @:var business_scope 经营范围
    """
    if not page_source:
        return
    base_dict = {}

    html = page_source.get('html')
    base_dict['history_name'] = history_name
    soup = bs(html, 'lxml')
    detail_value = soup.select("div.overview dd")
    detail_key = soup.select("div.overview dt")

    for key, value in zip(detail_key, detail_value):
        key = transfrom_base_name(key.text.strip(), source_id)
        base_dict[key] = value.text.strip()

    base_dict['create_time'] = now_time()
    base_dict['source_id'] = source_id

    ETL_JSON["jbxx"] = base_dict

    # etl_table_name = "etl_gsxt_home"
    # insert_mysql(etl_table_name, base_dict,source_id)

    print source_id + ":parse_html over!!!"

def parse_shareholder(page_source, source_id):
    """  解析股东及出资信息字段
         @:var partner_name 股东名称
         @:var partner_type 股东类型
         @:var bLicNo 证件号码
         @:var blicType_CN 证件类型
         @:var conDate 公示日期parse_shareholder
    """
    if not page_source:
        ETL_JSON["gdxx"] = []
        return

    gdxx = []
    for _shareholder in page_source:
        holder_detail_json = str_to_json(_shareholder.get("html"))
        datas = holder_detail_json.get("data")
        etl_table_name = "etl_gsxt_shareholder"

        for data in datas :
            shareholder = {}
            shareholder["partner_name"] = data.get("inv")
            shareholder["partner_type"] = clear_noise(data.get("invType_CN"))
            shareholder["bLicNo"] = clear_noise(data.get("bLicNo"))
            shareholder["blicType_CN"] = data.get("blicType_CN")
            shareholder["conDate"] = data.get("conDate")
            shareholder["invId"] = data.get("invId")
            gdxx.append(shareholder)

    ETL_JSON["gdxx"] = gdxx
    print source_id + ":parse_shareholder over!!!"

def parse_shareholder_detail(page_source, source_id) :
    """  解析股东及出资信息字段
         @:var acConAm 实缴额
         @:var subConAm 认缴额
         @:var acconDate 实缴出资日期
         @:var subconDate 认缴出资日期
         @:var subconForm_CN 认缴出资方式
         @:var acconForm_CN 实缴出资方式
    """
    if not page_source:
        return

    for _holder_details in page_source :
        holder_details = str_to_json(_holder_details.get("html"))
        datas = holder_details.get("data")
        ac_datas = datas[0]
        sub_datas = datas[1]

        gdxxs = ETL_JSON.get("gdxx")

        for gdxx in gdxxs:

            for ac_data in ac_datas :
                # etl_table_name = "etl_gsxt_shareholder_ac_detail"
                ac_invId = ac_data.get("invId")

                if ac_invId in gdxx.get("invId") :
                    gdxx["acConAm"] = ac_data.get("acConAm")
                    gdxx["acconDate"] = transfrom_timestrip(ac_data.get("conDate"))
                    gdxx["acconForm_CN"] = ac_data.get("conForm_CN")
                    gdxx["ac_invId"] = ac_data.get("invId")

            for sub_data in sub_datas :
                # etl_table_name = "etl_gsxt_shareholder_sub_detail"
                sub_invId = sub_data.get("invId")

                if sub_invId in gdxx.get("invId"):
                    gdxx["subConAm"] = sub_data.get("subConAm")
                    gdxx["subconDate"] = transfrom_timestrip(sub_data.get("conDate"))
                    gdxx["subconForm_CN"] = sub_data.get("conForm_CN")
                    gdxx["sub_invId"] = sub_invId

    print source_id + ":parse_shareholder_detail over!!!"

def parse_key_person(page_source, source_id):
    """  解析主要人员信息字段
         @:var name 主要人员姓名
         @:var position 主要人员职位
    """
    if not page_source:
        ETL_JSON["baxx"] = []
        return

    etl_table_name = "etl_gsxt_keyperson"
    baxx = []
    for _key_person in page_source :
        key_person_json = str_to_json(_key_person.get('html'))
        datas = key_person_json.get("data")

        for data in datas :
            tmp = {}
            tmp["name"] = clear_noise(data.get("name"))
            position = data.get("position_CN")
            tmp["position"] = transfrom_key_person_position(position)
            baxx.append(tmp)
    ETL_JSON["baxx"] = baxx
    print source_id + ":parse_key_person over!!!"

def parse_branch(page_source, source_id):
    """  解析分支机构信息字段
        @:var branch_name 分支机构名称
        @:var regNo 统一社会信用代码/注册号
        @:var regOrg 登记机关
    """
    if not page_source:
        ETL_JSON["fzjg"] = []
        return
    etl_table_name = "etl_gsxt_branch"
    fzjg = []
    for _branch in page_source :
        branch_json = str_to_json(_branch.get('html'))
        datas = branch_json.get("data")

        for data in datas :
            tmp = {}
            tmp["branch_name"] = data.get("brName")
            tmp["regNo"] = data.get("regNo")
            tmp["regOrg"] = data.get("regOrg_CN")
            fzjg.append(tmp)
    ETL_JSON["fzjg"] = fzjg
    print source_id + ":parse_branch over!!!"

def parse_alter_info(page_source, source_id):
    """  解析变更信息字段
         @:var alter_after 变更后内容
         @:var alter_brefore 变更前内容
         @:var alter_info 变更事项
         @:var alt_date 变更日期
    """
    if not page_source:
        ETL_JSON["bgxx"] = []
        return
    bgxx = []
    etl_table_name = "etl_gsxt_alterinfo"
    for _alter_infos in page_source :
        alter_infos = str_to_json(_alter_infos.get("html"))
        datas = alter_infos.get("data")
        for data in datas:
            tmp = {}
            tmp["altAf"] = data.get("altAf")
            tmp["altBe"] = data.get("altBe")
            tmp["altItem_CN"] = clear_noise(data.get("altItem_CN"))
            tmp["altDate"] = transfrom_timestrip(data.get("altDate"))
            bgxx.append(tmp)
    ETL_JSON["bgxx"] = bgxx
    print source_id + ":parse_alter_info over!!!"

def parse_trade_mark(page_source, source_id):
    """  商标详细信息
         @:var regNum 商标注册号
         @:var regAnncDate 注册公告日期
         @:var intCls 类别
         @:var regAnncIssue 注册公告期号
         @:var propertyBgnDate 商标专用权起日期
         @:var propertyEndDate 商标专用权止日期
         @:var coownerCnName 商标共有人信息
         @:var goodsCnName 商品/服务项目
    """
    if not page_source:
        ETL_JSON["sbxx"] = []
        return
    etl_table_name = "etl_gsxt_trademarkinfo"
    sbxx = []

    for _trade_mark in page_source :
        trade_mark_json = str_to_json(_trade_mark.get("html"))
        datas = trade_mark_json.get("data")
        for data in datas:
            tmp = {}
            tmp["regNum"] = data.get("regNum")
            tmp["regAnncDate"] = transfrom_timestrip(data.get("regAnncDate"))
            tmp["intCls"] = data.get("intCls")
            tmp["regAnncIssue"] = data.get("regAnncIssue")
            tmp["propertyBgnDate"] = transfrom_timestrip(data.get("propertyBgnDate"))
            tmp["propertyEndDate"] = transfrom_timestrip(data.get("propertyEndDate"))
            tmp["coownerCnName"] = data.get("coownerCnName")
            tmp["goodsCnName"] = clear_noise(data.get("goodsCnName")).strip()
            sbxx.append(tmp)
    ETL_JSON["sbxx"] = sbxx
    print source_id + ":parse_trade_mark over!!!"

def parse_spot_check_info(page_source, source_id):
    """  抽查检查结果信息
         @:var insAuth_CN 检查实施机关
         @:var insDate 日期
         @:var insType 类型 2:检查 1:抽查
         @:var insRes_CN 结果
    """
    if not page_source:
        ETL_JSON["ccjc"] = []
        return
    etl_table_name = "etl_gsxt_spotcheckinfo"
    ccjc = []
    for _spot_check in page_source :
        spot_check_json = str_to_json(_spot_check.get('html'))
        datas = spot_check_json.get("data")

        for data in datas:
            tmp = {}
            tmp["insAuth_CN"] = data.get("insAuth_CN")
            tmp["insDate"] = transfrom_timestrip(data.get("insDate"))
            tmp["insType"] = transfrom_insType(data.get("insType"))
            tmp["insRes_CN"] = data.get("insRes_CN")
            ccjc.append(tmp)
    ETL_JSON["ccjc"] = ccjc
    print source_id + ":parse_spot_check_info over!!!"

def ins_Licence_info(page_source, source_id):
    """  行政许可信息
         @:var licName_CN 许可文件名称
         @:var licNo 许可文件编号
         @:var valFrom 有效期自
         @:var valTo 有效期至
         @:var licAnth 许可机关
         @:var licItem 许可内容
    """
    if not page_source:
        ETL_JSON["xzxkbottom"] = []
        return
    etl_table_name = "etl_gsxt_inslicenceinfo"
    xzxkbottom = []
    for _info in page_source :
        ins_Licence_json = str_to_json(_info.get('html'))
        datas = ins_Licence_json.get("data")

        for data in datas :
            tmp = {}
            tmp["licName_CN"] = data.get("licName_CN")
            tmp["licNo"] = data.get("licNo")
            tmp["valFrom"] = transfrom_timestrip(data.get("valFrom"))
            tmp["valTo"] = transfrom_timestrip(data.get("valTo"))
            tmp["licAnth"] = data.get("licAnth")
            tmp["licItem"] = data.get("licItem")
            xzxkbottom.append(tmp)
    ETL_JSON["xzxkbottom"] = xzxkbottom
    print source_id + ":ins_Licence_info over!!!"

def mort_reg_info(page_source, source_id):
    """  动产抵押登记信息
         @:var morRegCNo 登记编号
         @:var regiDate 登记日期
         @:var publicDate 公示日期
         @:var regOrg_CN 登记机关
         @:var priClaSecAm 被担保债权数额
         @:var regCapCur_Cn 数额单位
    """
    if not page_source:
        ETL_JSON["dcdy"] = []
        return

    etl_table_name = "etl_gsxt_mortreginfo"
    dcdy = []
    for _mort_reg in page_source :
        mort_reg_json = str_to_json(_mort_reg.get('html'))
        datas = mort_reg_json.get("data")

        for data in datas :
            tmp = {}
            tmp["morRegCNo"] = data.get("morRegCNo")
            tmp["morReg_Id"] = data.get("morReg_Id")
            tmp["regiDate"] = transfrom_timestrip(data.get("regiDate"))
            tmp["publicDate"] = transfrom_timestrip(data.get("publicDate"))
            tmp["regOrg_CN"] = data.get("regOrg_CN")
            tmp["priClaSecAm"] = data.get("priClaSecAm")
            dcdy.append(tmp)
    ETL_JSON["dcdy"] = dcdy
    print source_id + ":mort_reg_info over!!!"

def mort_reg_details(page_source, source_id):
    if not page_source:
        return

    for detail in page_source:
        id = detail.get("id")
        xq_key = detail.get("xq_key")
        data = str_to_json(detail.get("html")).get('data')

        if 'mortregpersoninfo' == xq_key:
            parse_mort_reg_regpersoninfo(id, source_id, data)
            continue
        if 'mortCreditorRightInfo'== xq_key:
            parse_mort_reg_creditorRightInfo(id, source_id, data)
            continue
        if 'getMortAltItemInfo'== xq_key:
            # parse_mort_reg_altItemInfo(id, source_id, data)
            continue
        if 'getMortRegCancelInfo'== xq_key:
            mort_reg_cancelInfo(id, source_id, data)
            continue
        if 'mortGuaranteeInfo'== xq_key:
            parse_mort_reg_guaranteeInfo(id, source_id, data)
            continue

def parse_mort_reg_regpersoninfo(id, source_id, data) :
    """  动产抵押登记信息 详情 抵押权人信息
         @:var morReg_Id
         @:var more 抵押权人名称
         @:var bLicType_CN 抵押权人证照类型
         @:var bLicNo 证照号码
         @:var morLoc 住所地
    """
    etl_table_name ="etl_gsxt_mortreg_regpersoninfo"
    dcdys = ETL_JSON.get("dcdy")
    for dcdy in dcdys:
        dcdy_id = dcdy.get("morReg_Id")

        for _regpersoninfo in data:
            morReg_Id = _regpersoninfo.get("morReg_Id")

            if morReg_Id in dcdy_id:
                dcdy["more"] = _regpersoninfo.get("more")
                dcdy["bLicType_CN"] = _regpersoninfo.get("bLicType_CN")
                dcdy["bLicNo"] = _regpersoninfo.get("bLicNo")
                dcdy["morLoc"] = _regpersoninfo.get("morLoc")

    print source_id + ":parse_mort_reg_regpersoninfo over!!!"

def parse_mort_reg_creditorRightInfo(id, source_id, data) :
    """  动产抵押登记信息 详情 被担保主债权信息
         @:var priClaSecKind_CN 种类
         @:var regCapCur_CN 币种
         @:var priClaSecAm 数额
         @:var warCov 担保的范围
         @:var pefPerForm, pefPerTo 债务人履行债务的期限
         @:var creditor_remark 备注
    """
    etl_table_name = "etl_gsxt_mortreg_creditorrightinfo"
    dcdys = ETL_JSON.get("dcdy")
    for dcdy in dcdys:
        dcdy_id = dcdy.get("morReg_Id")

        for _creditorRightInfo in data:
            morReg_Id = _creditorRightInfo.get("morReg_Id")

            if morReg_Id in dcdy_id:
                dcdy["priClaSecKind_CN"] = _creditorRightInfo.get("priClaSecKind_CN")
                dcdy["regCapCur_CN"] = _creditorRightInfo.get("regCapCur_CN")
                dcdy["priClaSecAm"] = _creditorRightInfo.get("priClaSecAm")
                dcdy["warCov"] = _creditorRightInfo.get("warCov")
                dcdy["pefPerForm"] = transfrom_timestrip(_creditorRightInfo.get("pefPerForm"))
                dcdy["pefPerTo"] = transfrom_timestrip(_creditorRightInfo.get("pefPerTo"))
                dcdy["creditor_remark"] = _creditorRightInfo.get("remark")

    print source_id + ":parse_mort_reg_creditorRightInfo over!!!"

def parse_mort_reg_guaranteeInfo(id, source_id, data) :
    """  动产抵押登记信息 详情 抵押物信息信息
         @:var guaDes 数量、质量、状况、所在地等情况
         @:var guaName 抵押物名称
         @:var own 所有权或使用权归属
         @:var guarantee_remark 备注
    """

    etl_table_name = "etl_gsxt_mortreg_guaranteeinfo"
    dcdys = ETL_JSON.get("dcdy")
    for dcdy in dcdys:
        dcdy_id = dcdy.get("morReg_Id")

        for _guaranteeInfo in data:
            morReg_Id = _guaranteeInfo.get("morReg_Id")

            if morReg_Id in dcdy_id:
                dcdy["guaDes"] = _guaranteeInfo.get("guaDes")
                dcdy["guaName"] = _guaranteeInfo.get("guaName")
                dcdy["own"] = _guaranteeInfo.get("own")
                dcdy["guarantee_remark"] = _guaranteeInfo.get("remark")

    print source_id + ":parse_mort_reg_guaranteeInfo over!!!"

def parse_mort_reg_altItemInfo(id, source_id, data) :
    """  动产抵押登记信息 详情 变更信息
    """
    

    for altItemInfo in data:
        AltItemInfo_json = str_to_json(altItemInfo[0])
        datas = AltItemInfo_json.get("data")

        for data in datas:
            pass

def mort_reg_cancelInfo(id, source_id, data) :
    """  动产抵押登记信息 详情 注销信息
         @:var morRegCNo 登记编号
         @:var cancel_regiDate 登记日期
         @:var regOrg_CN 登记机关
         @:var remark 备注
         @:var canDate 注销日期
         @:var morCanRea_CN 注销原因
    """
    etl_table_name = "etl_gsxt_mortreg_cancelinfo"
    dcdys = ETL_JSON.get("dcdy")

    for dcdy in dcdys:
        dcdy_id = dcdy.get("morReg_Id")

        for _cancelInfo in data :
            morReg_Id = _cancelInfo.get("morReg_Id")

            if morReg_Id in dcdy_id:
                dcdy["morRegCNo"] = _cancelInfo.get("morRegCNo")
                dcdy["cancel_regiDate"] = transfrom_timestrip(_cancelInfo.get("regiDate"))
                dcdy["canDate"] = transfrom_timestrip(_cancelInfo.get("canDate"))
                dcdy["regOrg_CN"] = _cancelInfo.get("regOrg_CN")
                dcdy["morCanRea_CN"] = _cancelInfo.get("morCanRea_CN")

    print source_id + ":mort_reg_cancelInfo over!!!"

def parse_ins_Inv(page_source, source_id):
    """  解析股东及出资信息字段
         @:var inv 股东名称
         @:var subSum 认缴额（万元）
         @:var aubSum 实缴额（万元）

         @:var subDetails 认缴明细
         @:var aubDetails 实缴明细

         @:var subConForm_CN 认缴出资方式
         @:var subConAm 认缴出资金额(万元)
         @:var currency 认缴出资日期
         @:var sub_publicDate 公示日期

         @:var acConFormName 实缴出资方式
         @:var acConAm 实缴出资金额(万元)
         @:var conDate 实缴出资日期
         @:var ac_publicDate 实缴公示日期
    """
    if not page_source:
        ETL_JSON["gdxxbottom"] = []
        return

    etl_table_name = "etl_gsxt_insinvinfo"
    gdxxbottom = []
    for _ins_Inv in page_source:
        ins_Inv_json = str_to_json(_ins_Inv.get('html'))
        datas = ins_Inv_json.get("data")

        for data in datas :
            tmp = {}
            tmp["inv"] = data.get("inv")
            tmp["subSum"] = data.get("subSum")
            tmp["aubSum"] = data.get("aubSum")
            subDetails = data.get("subDetails")
            aubDetails = data.get("aubDetails")

            for (subDetail, aubDetail) in zip(subDetails, aubDetails) :
                tmp["subConForm_CN"] = subDetail.get("subConForm_CN")
                tmp["subConAm"] = subDetail.get("subConAm")
                tmp["currency"] = transfrom_timestrip(subDetail.get("currency"))
                tmp["sub_publicDate"] = transfrom_timestrip(subDetail.get("publicDate"))
                tmp["sub_invId"] = subDetail.get("invId")
                tmp["sub_subId"] = subDetail.get("subId")

                tmp["conDate"] = transfrom_timestrip(aubDetail.get("conDate"))
                tmp["ac_publicDate"] = transfrom_timestrip(aubDetail.get("publicDate"))
                tmp["acConFormName"] = aubDetail.get("acConFormName")
                tmp["acConAm"] = aubDetail.get("acConAm")
                tmp["ac_invId"] = aubDetail.get("invId")
                tmp["ac_paidId"] = aubDetail.get("paidId")

            gdxxbottom.append(tmp)

    ETL_JSON["gdxxbottom"] = gdxxbottom
    print source_id + ":parse_ins_Inv over!!!"

def other_Licence_detail_info(page_source, source_id):
    """  行政许可信息
         @:var licName_CN 许可文件名称
         @:var licNo 许可文件编号
         @:var valFrom 有效期自
         @:var valTo 有效期至
         @:var licAnth 许可机关
         @:var licItem 许可内容
    """
    if not page_source:
        ETL_JSON["xzxktop"] = []
        return
    etl_table_name = "etl_gsxt_otherlicencedetailinfo"
    xzxktop = []
    for _other_Licence_detail_info in page_source:
        other_Licence_json = str_to_json(_other_Licence_detail_info.get('html'))
        datas = other_Licence_json.get("data")

        for data in datas :
            tmp = {}
            tmp["licName_CN"] = data.get("licName_CN")
            tmp["licNo"] = data.get("licNo")
            tmp["valFrom"] = transfrom_timestrip(data.get("valFrom"))
            tmp["valTo"] = transfrom_timestrip(data.get("valTo"))
            tmp["licAnth"] = data.get("licAnth")
            tmp["licItem"] = data.get("licItem").strip()
            tmp["licId"] = data.get("licId")

            xzxktop.append(tmp)

    ETL_JSON["xzxktop"] = xzxktop
    print source_id + ":other_Licence_detail_info over!!!"

def stak_qualit(page_source, source_id) :
    """  股权出质登记信息
         @:var equityNo 登记编号
         @:var pledgor 出质人
         @:var pledBLicNo 证照/证件号码
         @:var impAm 出质股权数额
         @:var impOrg 质权人
         @:var pledAmUnit 出质单位  1/2  万元/万股
         @:var impOrgBLicNo 证照/证件号码
         @:var equPleDate 股权出质设立登记日期
         @:var type 状态 2/无效  1/有效
         @:var publicDate 公示日期
    """
    etl_table_name = "etl_gsxt_stakqualitinfo"
    if not page_source:
        ETL_JSON["gqcz"] = []
        return

    gqcz = []
    for _stak_qualit_info in page_source:
        stak_qualit_json = str_to_json(_stak_qualit_info.get('html'))
        datas = stak_qualit_json.get("data")

        for data in datas :
            tmp = {}
            tmp["equityNo"] = data.get("equityNo")
            tmp["pledgor"] = data.get("pledgor")
            tmp["pledBLicNo"] = data.get("pledBLicNo")
            tmp["impAm"] = data.get("impAm")
            tmp["impOrg"] = data.get("impOrg")
            tmp["pledAmUnit"] = transfrom_stack_type(data.get("pledAmUnit"))
            tmp["impOrgBLicNo"] = data.get("impOrgBLicNo")
            tmp["equPleDate"] = transfrom_timestrip(data.get("equPleDate"))
            tmp["status"] = transfrom_stack_status(data.get("type"))
            tmp["publicDate"] = transfrom_timestrip(data.get("publicDate"))
            gqcz.append(tmp)

    ETL_JSON["gqcz"] = gqcz
    print source_id + ":stak_qualit over!!!"

def ins_alter_stock_info(page_source, source_id) :
    """  股权变更信息
         @:var altDate 股权变更日期
         @:var transAmPrAf 变更后股权比例
         @:var transAmPrBf 变更前股权比例
         @:var inv 股东
         @:var publicDate 公示日期
    """
    etl_table_name = "etl_gsxt_insalterstockinfo"
    if not page_source:
        ETL_JSON["gqbgbottom"] = []
        return
    gqbgbottom = []

    for _ins_alter_stock in page_source:
        ins_alter_stock_json = str_to_json(_ins_alter_stock.get('html'))
        datas = ins_alter_stock_json.get("data")

        for data in datas:
            tmp = {}
            tmp["inv"] = data.get("inv")
            tmp["transAmPrAf"] = data.get("transAmPrAf")
            tmp["transAmPrBf"] = data.get("transAmPrBf")
            tmp["altDate"] = transfrom_timestrip(data.get("altDate"))
            tmp["publicDate"] = transfrom_timestrip(data.get("publicDate"))

            gqbgbottom.append(tmp)

    ETL_JSON["gqbgbottom"] = gqbgbottom
    print source_id + ":ins_alter_stock_info over!!!"

def simple_cancel(page_source, source_id):
    """  企业简易注销公告信息
         @:var entName 企业名称
         @:var noticeFrom 公告期起
         @:var noticeTo 公告期止
         @:var regOrg 登记机关
         #需要测一下，数据格式不同于其他模块
    """
    if not page_source:
        ETL_JSON["zxggbottom"] = []
        return
    zxggbottom = []
    etl_table_name = "etl_gsxt_simplecancel"

    for _simple_cancel in page_source:
        simple_cancel_json = str_to_json(_simple_cancel.get('html'))
        # datas = simple_cancel_json.get("data")
        tmp = {}
        tmp["entName"] = simple_cancel_json.get("entName")
        tmp["noticeFrom"] = transfrom_timestrip(simple_cancel_json.get("noticeFrom"))
        tmp["noticeTo"] = transfrom_timestrip(simple_cancel_json.get("noticeTo"))
        tmp["regOrg"] = simple_cancel_json.get("regOrg")
        tmp["id"] = _simple_cancel[1]
        zxggbottom.append(tmp)

    ETL_JSON["zxggbottom"] = zxggbottom
    print source_id + ":simple_cancel over!!!"

def ill_detail(page_source, source_id) :
    """  列入严重违法失信企业名单（黑名单）信息
         @:var decOrg_CN 作出决定机关(列入)
         @:var serILLRea_CN 列入严重违法失信企业名单（黑名单）原因
         @:var abntime 列入日期
         @:var reDecOrg_CN 作出决定机关(移出)
         @:var remExcpRes_CN 移出严重违法失信企业名单（黑名单）原因
         @:var remDate 移出日期
    """
    # 缺个类别
    if not page_source:
        ETL_JSON["hmdtop"] = []
        return
    etl_table_name = "etl_gsxt_illinfo"
    hmdtop = []

    for _ill_detail in page_source:
        ill_detail_json = str_to_json(_ill_detail.get('html'))
        datas = ill_detail_json.get("data")

        for data in datas:
            tmp = {}
            tmp["decOrg_CN"] = data.get("decOrg_CN")
            tmp["serILLRea_CN"] = data.get("serILLRea_CN")
            tmp["abntime"] = transfrom_timestrip(data.get("abntime"))
            tmp["remExcpRes_CN"] = data.get("remExcpRes_CN")
            tmp["reDecOrg_CN"] = data.get("reDecOrg_CN")
            tmp["remDate"] = transfrom_timestrip(data.get("remDate"))
            hmdtop.append(tmp)

    ETL_JSON["hmdtop"] = hmdtop
    print source_id + ":ill_detail over!!!"

def ent_bus_excep(page_source, source_id) :
    """  列入经营异常名录信息
         @:var abntime 列入日期
         @:var speCause_CN 列入经营异常名录原因
         @:var decOrg_CN 作出决定机关(列入)
         @:var remExcpRes_CN 移出经营异常名录原因
         @:var reDecOrg_CN 作出决定机关(移出)
         @:var remDate 移出日期
    """
    if not page_source:
        ETL_JSON["jyyctop"] = []
        return
    etl_table_name = "etl_gsxt_entbusexcep"
    jyyctop = []
    for _ent_bus_excep in page_source:
        ent_bus_excep_json = str_to_json(_ent_bus_excep.get('html'))
        datas = ent_bus_excep_json.get("data")

        for data in datas:
            tmp = {}
            tmp["abntime"] = transfrom_timestrip(data.get("abntime"))
            tmp["speCause_CN"] = data.get("speCause_CN")
            tmp["decOrg_CN"] = data.get("decOrg_CN")
            tmp["remExcpRes_CN"] = data.get("remExcpRes_CN")
            tmp["reDecOrg_CN"] = data.get("reDecOrg_CN")
            tmp["remDate"] = transfrom_timestrip(data.get("remDate"))
            jyyctop.append(tmp)

    ETL_JSON["jyyctop"] = jyyctop
    print source_id + ":ent_bus_excep over!!!"

def parse_assist(page_source, source_id) :
    """  司法协助
         @:var inv 被执行人
         @:var froAm 股权数额
         @:var froAuth 执行法院
         @:var executeNo 执行通知书文号
         @:var frozState 类型|状态 失效:3  冻结:1  解除冻结:2
         @:var frozState_CN 状态
    """
    if not page_source:
        ETL_JSON["sfxz"] = []
        return
    sfxz = []
    etl_table_name = "etl_gsxt_assist"
    for parse_assist in page_source:
        parse_assist_json = str_to_json(parse_assist.get('html'))
        datas = parse_assist_json.get("data")

        for data in datas:
            tmp = {}
            tmp["inv"] = data.get("inv")
            tmp["froAm"] = data.get("froAm")
            tmp["froAuth"] = data.get("froAuth")
            tmp["executeNo"] = data.get("executeNo")
            frozState_CN = data.get("frozState_CN")
            frozState = data.get("frozState")
            tmp["frozState"] = frozState
            if not frozState_CN:
                frozState_CN = transfrom_check_type(frozState)
            tmp["frozState_CN"] = frozState_CN
            sfxz.append(tmp)

    ETL_JSON["sfxz"] = sfxz
    print source_id + ":parse_assist over!!!"

def parse_liquidation(page_source, source_id) :
    """  清算信息
         @:var addr 未知
         @:var cerNo 未知
         @:var cerType 未知
         @:var liId 未知
         @:var ligpriSign 1负责人 2清算组成员
         @:var limeId 未知
         @:var liqMem 清算人姓名
         @:var pripId 未知
    """
    if not page_source:
        ETL_JSON["qsxx"] = []
        return
    etl_table_name = "etl_gsxt_liquidation"
    qsxx = []
    for _liquidation in page_source:
        parse_assist_json = str_to_json(_liquidation.get('html'))
        datas = parse_assist_json.get("data")

        for data in datas:
            tmp = {}
            tmp["addr"] = data.get("addr")
            tmp["cerNo"] = data.get("cerNo")
            tmp["cerType"] = data.get("cerType")
            tmp["liId"] = clear_noise(data.get("liId"))
            tmp["ligpriSign"] = data.get("ligpriSign")
            tmp["limeId"] = clear_noise(data.get("limeId"))
            tmp["liqMem"] = clear_noise(data.get("liqMem"))
            tmp["pripId"] = data.get("pripId")
            qsxx.append(tmp)

    ETL_JSON["qsxx"] = qsxx
    print source_id + ":parse_liquidation over!!!"

def parse_DrRaninsResUrl(page_source, source_id) :
    """  双随机抽查结果信息
             @:var insAuth 抽查机关
             @:var insDate 抽查完成日期
             @:var pripId 未知
             @:var raninsTypeName 抽查类型
             @:var raninsPlanId 抽查计划编号
             @:var raninsPlaneName 抽查计划名称
             @:var raninsTaskName 抽查任务名称
             @:var raninsTaskId 抽查任务编号
        """
    if not page_source:
        ETL_JSON["sjxx"] = []
        return
    etl_table_name = "etl_gsxt_drraninsres"
    sjxx = []
    for _drraninsre in page_source:
        drraninsre_json = str_to_json(_drraninsre.get('html'))
        datas = drraninsre_json.get("data")

        for data in datas:
            tmp = {}
            tmp["insAuth"] = data.get("insAuth")
            tmp["insDate"] = transfrom_timestrip(data.get("insDate"))
            tmp["pripId"] = data.get("pripId")
            tmp["raninsTypeName"] = data.get("raninsTypeName")
            tmp["raninsPlanId"] = data.get("raninsPlanId")
            tmp["raninsPlaneName"] = data.get("raninsPlaneName")
            tmp["raninsTaskName"] = data.get("raninsTaskName")
            tmp["raninsTaskId"] = data.get("raninsTaskId")
            sjxx.append(tmp)

    ETL_JSON["sjxx"] = sjxx
    print source_id + ":parse_DrRaninsResUrl over!!!"

def parse_ins_Punishment(page_source, source_id):
    """  行政处罚信息（单页）
         @:var penDecNo 决定书文号
         @:var illegActType 违法行为类型
         @:var penContent 行政处罚内容
         @:var penAuth_CN 决定机关名称
         @:var penDecIssDate 处罚决定日期
         @:var publicDate 公示日期
         @:var pripId 未知
         @:var caseId 未知
    """
    if not page_source:
        ETL_JSON["xzcfbottom"] = []
        return
    etl_table_name = "etl_gsxt_inspunishmentinfo"
    xzcfbottom = []
    for _punishmentdetail in page_source:
        punishmentdetail = str_to_json(_punishmentdetail.get('html'))
        datas = punishmentdetail.get("data")

        for data in datas:
            tmp = {}
            tmp["penDecNo"] = data.get("penDecNo")
            tmp["illegActType"] = data.get("illegActType")
            tmp["penContent"] = data.get("penContent")
            tmp["penAuth_CN"] = data.get("penAuth_CN")
            tmp["publicDate"] = transfrom_timestrip(data.get("publicDate"))
            tmp["penDecIssDate"] = transfrom_timestrip(data.get("penDecIssDate"))
            tmp["pripId"] = data.get("pripId")
            tmp["caseId"] = data.get("caseId")
            xzcfbottom.append(tmp)

    ETL_JSON["xzcfbottom"] = xzcfbottom
    print source_id + ":parse inspunishmentinfo over!!!"

def parse_punishmentdetailinfo(page_source, source_id) :
    """  行政处罚信息（首页）
         @:var penDecNo 决定书文号
         @:var illegActType 违法行为类型
         @:var penContent 行政处罚内容
         @:var penAuth_CN 决定机关名称
         @:var penDecIssDate 处罚决定日期
         @:var publicDate 公示日期
         @:var pripId 未知
         @:var caseId 未知
    """
    if not page_source:
        ETL_JSON["xzcftop"] = []
        return

    etl_table_name = "etl_gsxt_punishmentdetailinfo"
    xzcftop = []
    for _punishmentdetail in page_source:
        punishmentdetail = str_to_json(_punishmentdetail.get('html'))
        datas = punishmentdetail.get("data")

        for data in datas:
            tmp = {}
            tmp["penDecNo"] = data.get("penDecNo")
            tmp["illegActType"] = data.get("illegActType")
            tmp["penContent"] = data.get("penContent")
            tmp["penAuth_CN"] = data.get("penAuth_CN")
            tmp["publicDate"] = transfrom_timestrip(data.get("publicDate"))
            tmp["penDecIssDate"] = transfrom_timestrip(data.get("penDecIssDate"))
            tmp["pripId"] = data.get("pripId")
            tmp["caseId"] = data.get("caseId")
            xzcftop.append(tmp)

    ETL_JSON["xzcftop"] = xzcftop
    print source_id + ":parse_punishmentdetailinfo over!!!"

def transfrom_timestrip(_t):
    if not _t :
        return ""
    if str(_t).startswith('-'):
        _t = _t/1000
        str_time = datetime.datetime(1970, 1, 2) + datetime.timedelta(seconds=_t)
        return str_time.__str__()[2:]
    if _t >= 253402185600000:
        return "9999年12月31日"
    if _t :
        _t = _t / 1000
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(_t)))


def transfrom_stack_status(status) :
    if "1" == status :
        return u"有效"
    if "2" == status :
        return u"无效"
    return status

def transfrom_stack_type(pledAmUnit):
    """ pledAmUnit 出质单位  1/2  万元/万股"""
    if u"2" == pledAmUnit :
        return u"万股"
    if u"1" == pledAmUnit :
        return u"万元"
    return ""

def transfrom_check_type(insType):
    if u"1" == insType:
        return u"股权冻结|冻结"
    if u"2" == insType:
        return u"股权冻结|解除冻结"
    if u"3" == insType:
        return u"股权冻结|失效"
    if u"" == insType:
        return u"股权变更"
    return insType

def transfrom_insType(insType):
    if u"1" == insType:
        return u"抽查"
    if u"2" == insType:
        return u"检查"
    if u"0" == insType:
        return u""
    return insType

def transfrom_key_person_position(position):

    if  position.__len__() < 20 :
        return position

    enum_position={"mNgwA7SgNgUiV8OxEoM": u"监事", "mNgGERgAxI7HIizSNC7":u"监事",
                   "qWUMUgDQRBFDwsrsbGw": u"董事", "mNgGERgOQE+PrCJWIXl": u"董事",
                   "rWVQUSDYRjHJ5MOiUw6": u"董事长", "t2VMUgDQRBFQwhiZScW": u"董事长",
                   "sWVX2SVYRzHHzNHcsSR": u"总经理", "tWVQUSDYRjHPzNJuiQd": u"总经理",
                   "r2YcUScYRzHXzknk8hk": u"董事兼总经理", "q2XT2RcURTGnxgR8WRT": u"监事会主席",
                   "r2WUYSUURTHx1irh8RK": u"执行董事", "uWWTUREURTHx8hIRiRJ": u"执行董事",
                   "r2Yf2SVURjHr2uuyYzJ": u"董事长兼经理", "p2VQUTDURzH":u"负责人",
                   "r2UT0REURTGr5G0eCJJ": u"经理", "rWWQWRcURSGn4roYoSI":u"副董事长",
                   "q2WT2RcURSHn4qoGiGq": u"首席代表", "rWXQWScQRTHR0SsWqGH": u"其他人员",
                   "q2WT2TcURDHn1irhwgV": u"独立董事", "r2WX2RbURzHr4iYiRE1": u"副总经理",
                   "s2XcWSUYRzHX2dOcsZk": u"董事,总经理", "s2WQUTDURzHZzLJdEuS": u"职工监事",
                   "s2YT0TDYRjHf5J0yMhk": u"董事,董事长", "q2WT0TDYRjHf2YmmZGk": u"监事长",
                   "s2WT0TDYRjHJ0mH6ZIk": u"职工董事", "mNgoA7QAuIpBNSw4JIo": u"厂长",
                   "DhklEQVR42sVYX2RbURi": u"职工代表监事", "DZ0lEQVR42q2Xb0RdYRjAryTJNSbT": u"董事会秘书",
                   "s2XbWRbURjHIyr2ocpM": u"董事长,经理", "VQUTDURzH/5J0mJhJ": u"副经理",
                   "sWXb2TVURjHryvTi2tM": u"董事,经理", "s2Xf2TUYRzHvyanP2Yk": u"董事,经理",
                   "XQUREURSGR4sko02L": u"董事,监事", "qWWX2TbURTHfyr6MD": u"外部监事",
                   "rWXUUSkURTHxxhJ1pCs": u"董事,行长", "rVYX2SbURT": u"监事会副主席",
                   "sWXX2RbURzHIyL6EKVi": u"监事主席", "q2XT2RcURTGr4hRNbKp": u"监事主席",
                   "Xf2TUYRzHv2bOZEaS": u"董事、经理", "sWYUUSkURTHP0nWGsMa": u"董事,监事长",
                   "sWXX2RbURzHI6JqolTM": u"董事、副行长", "tWYT0SDYRzHX5NJZiTZ": u"监事长,监事",
                   "s1YX2RbYRSPipiIMlEz": u"监事、召集人", "tWYUURDURjHk6SHjEz2": u"董事长,董事",
                   "q2UIUhDQRjHL4gsPAST": u"其他"}

    enum_keys = enum_position.keys()
    for key in enum_keys:
        if key in position:
            return enum_position[key]

    return "未定义职位"


def transfrom_base_name(chinese_name, source_id) :
    """  首页字段
         @:var social_credit_code 统一社会信用代码/注册号
         @:var company_name 企业名称/名称
         @:var company_type 类型/组成形式
         @:var legaler 法定代表人
         @:var reg_capital 注册资本 reg="register"
         @:var business_began 成立日期/注册日期
         @:var bLicNo 营业期限自
         @:var business_end 营业期限至
         @:var reg_ins 登记机关 reg="register" ins = "institution"
         @:var approval_date 核准日期
         @:var reg_status 登记状态 reg="register"
         @:var business_scope 经营范围
         @:var address 营业场所：/住所
     """
    all_key_name = {
     u"统一社会信用代码" : "social_credit_code",
     u"注册号": "social_credit_code",
     u"企业名称": "company_name",
     u"名称": "company_name",
     u"类型": "company_type",
     u"组成形式": "company_type",
     u"法定代表人": "legaler",
     u"负责人": "legaler",
     u"经营者": "legaler",
     u"注册资本": "reg_capital",
     u"成立日期": "establish_date",
     u"注册日期": "establish_date",
     u"营业期限自": "business_began",
     u"经营期限自": "business_began",
     u"营业期限至": "business_end",
     u"经营期限至": "business_end",
     u"登记机关": "reg_ins",
     u"核准日期": "approval_date",
     u"登记状态": "reg_status",
     u"经营范围": "business_scope",
     u"营业场所": "address",
     u"住所": "address",
     u"经营场所": "address"
    }
    for key, value in all_key_name.iteritems() :
        if key in chinese_name:
            return value

    print source_id, chinese_name.encode("utf8")
    raise (u"key name is not compelte, didn't include chinese_name ")

def transfrom_ligpriSign(ligpriSign):
    if u"1" in ligpriSign:
        return "清算组负责人"
    if u"2" in ligpriSign:
        return "清算组成员"
    return "未定义成员"

def eval_to_json(json_str):
    #json_data = json.loads(json_str.encode("utf8", "ignore"))
    return eval(json_str)

def str_to_json(json_str):
    return json.loads(json_str.encode("utf8", "ignore"))

def now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def insert_mysql(table, model):
    dao.insert_dic(table, model)

def deal_sources(page_sources, source_id):
    # 缺少企业注销公告
    # 40f308de-a451-11e8-ac0c-0242ac110006
    # temp = eval_to_json(page_sources)
    # datas = temp.get("page_sources")
    datas =  page_sources
    history_name = datas.get("search_item").get("history_name")
    # history_name = u','.join(history_name_list)
    parse_html(datas.get("jbxx"), history_name, source_id)
    parse_shareholder(datas.get("gdxx"), source_id) # parse_shareholder
    parse_shareholder_detail(datas.get("gdxq_page_list"), source_id) # parse_shareholder_detail
    parse_alter_info(datas.get("bgxx"), source_id) # parse_alter_info
    parse_key_person(datas.get("baxx"), source_id) # 关键人 parse_key_person
    parse_branch(datas.get("fzjg"), source_id) # parse_branch
    mort_reg_info(datas.get("dcdy"), source_id) # mort_reg_info
    mort_reg_details(datas.get("dcdy_xq_list"), source_id)
    stak_qualit(datas.get("gqcz"), source_id) # stak_qualit
    other_Licence_detail_info(datas.get("xzxktop"), source_id) # 行政许可 other_Licence_detail_info
    parse_assist(datas.get("sfxz"), source_id) # parse_assist
    parse_punishmentdetailinfo(datas.get("xzcftop"), source_id) # parse_punishmentdetailinfo
    ent_bus_excep(datas.get("jyyctop"), source_id) # ent_bus_excep
    ill_detail(datas.get("hmdtop"), source_id) # ill_detail
    parse_liquidation(datas.get("qsxx"), source_id) # parse_liquidation
    parse_spot_check_info(datas.get("ccjc"), source_id)  # parse_spot_check_info
    ins_Licence_info(datas.get("xzxkbottom"), source_id)  # ins_Licence_info
    parse_ins_Punishment(datas.get("xzcfbottom"), source_id)  # parse_ins_Punishment 缺少
    parse_DrRaninsResUrl(datas.get("sjxx"), source_id)  # parse_DrRaninsResUrl
    parse_ins_Inv(datas.get("gdxxbottom"), source_id)  # parse_ins_Inv
    ins_alter_stock_info(datas.get("gqbgbottom"), source_id) # ins_alter_stock_info
    simple_cancel(datas.get("zxggbottom"), source_id) # simple_cancel


# def query_by_id():
#     quer()


def select_source_to_parse():
    page = 0
    PAGE_SIZE = 10
    while True:
        select_sql = 'SELECT id, source_id, company_uuid, company_key, page_sources FROM gsxt_page_json WHERE etl_status=0 LIMIT {}, {}'.format(page, PAGE_SIZE)
        try:
            result_list = dao.query(select_sql)
            for data_id, source_id, company_uuid, company_key, page_sources in result_list:
                status = 'success'
                page_source_dict = json.loads(page_sources)
                task_id = page_source_dict['seed_dict']['task_id']
                total_cnt = 1
                if page_source_dict['status'] == Status.SUCCESS:
                    try:
                        deal_sources(page_source_dict, source_id)
                        status = 'success'
                    except Exception:
                        error_msg = u'解析失败，task_id: {}, data_id: {}, 原因:{}'.format(task_id, data_id, traceback.format_exc())
                        status = 'fail'
                        logger.error(error_msg)
                elif page_source_dict['status'] == Status.NON_COMPANY:
                    status = 'no_record'
                    total_cnt = 0
                elif page_source_dict['status'] == Status.EXCEPTION:
                    status = 'fail'
                try:
                    save_dict = {
                        'task_id': task_id,
                        'status': status,
                        'total_cnt': total_cnt,
                        'company_uuid': company_uuid,
                        "source_id": source_id,
                        "create_time": now_time(),
                        "company_json": json.dumps(ETL_JSON, ensure_ascii=False)
                    }
                    insert_mysql("etl_gsxt_page_json", save_dict)
                    update_etl_status("gsxt_page_json", source_id, 1)
                    logger.info('解析完成,任务id:{}'.format(save_dict['task_id']))
                except Exception:
                    logger.error(u'存储到数据库异常: {}'.format(traceback.format_exc()))

            if len(result_list) == 0 or len(result_list) != PAGE_SIZE:
                logger.info(u'发送种子到队列完成')
                page = 0
                break
        except Exception as e:
            logger.error(str(e))

def etl_start():
    while True:
        try:
            logger.info('开始查询数据并解析')
            select_source_to_parse()
            logger.info('解析完毕')
        except Exception:
            logger.error(u'解析失败：{}'.format(traceback.format_exc()))

        time.sleep(12)


# def etl_start():
#
#     results = get_source_id()
#
#     for result in results:
#     #     result = error_test("1024d988-a480-11e8-b5bb-0242ac110006")[0]
#         source_id = result[0]
#         page_sources = result[1]
#         deal_sources(page_sources, source_id)
#
#         insert_mysql("etl_gsxt_page_json", {"source_id": source_id,
#                                             "create_time": now_time(),
#                                             "company_json": str(ETL_JSON)
#                                             })
#         update_etl_status("gsxt_page_json", source_id, 1)
#
# etl_start()


if __name__ == '__main__':
    etl_start()

