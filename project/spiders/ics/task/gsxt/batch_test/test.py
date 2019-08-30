# coding=utf-8






# @retry(exceptions=LogicException, tries=3, delay=1, logger=logger)
# def init_gdxx_page_list():
#     url = '{}{}'.format(host, value_dict['uri_dict']['gdxx_uri'])
#     data = {
#         'draw': 1,
#         'start': 0,
#         'length': 5
#     }
#     resp = send_request('post', url, data)
#     value_dict['gdxx_page_list'] = get_total_page(resp.text)
#
#
# @retry(exceptions=LogicException, tries=3, delay=1, logger=logger)
# def iter_gdxx_list():
#     page_dict['gdxx'] = []
#     url = '{}{}'.format(host, value_dict['uri_dict']['gdxx_uri'])
#     for page in value_dict['gdxx_page_list']:
#         data = {
#             "draw": page,
#             "start": (page - 1) * 5,
#             "length": 5
#         }
#         resp = send_request('post', url, data)
#         page_dict['gdxx'].append({
#             'page': page,
#             'html': resp.text
#         })
#         gdxq_id_list = get_xqid_list(resp.text, 'invId')
#         value_dict['gdxq_id_list'].extend(gdxq_id_list)
#
#
# def iter_gdxq_list():
#     for gdxq_id in value_dict['gdxq_id_list']:
#         url = '{}/corp-query-entprise-info-shareholderDetail-{}.html'.format(host, gdxq_id)
#         resp = send_request('get', url)
#         page_dict['gdxq_page_list'].append({
#             'id': gdxq_id,
#             'html': resp.text
#         })




# def init_baxx_page_list():
#     url = '{}{}'.format(host, value_dict['uri_dict']['baxx_uri'])
#     resp = send_request('get', url)
#     value_dict['baxx_page_list'] = get_total_page(resp.text)
#     pass
#
#
# def iter_baxx_list():
#     page_dict['baxx'] = []
#     baxx_page_list = value_dict['baxx_page_list']
#     for page in baxx_page_list:
#         url = '{}{}?start={}'.format(host, value_dict['uri_dict']['baxx_uri'], (page - 1) * 16)
#         resp = send_request('get', url)
#         page_dict['baxx'].append({
#             'page': page,
#             'html': resp.text
#         })
#
#
# def init_bgxx_page():
#     url = '{}{}'.format(host, value_dict['uri_dict']['bgxx_uri'])
#     data = {
#         "draw": 1,
#         "start": 0,
#         "length": 5
#     }
#     resp = send_request('post', url, data=data)
#     value_dict['bgxx_page_list'] = get_total_page(resp.text)
#
#
# def iter_bgxx_page():
#     page_dict['bgxx'] = []
#     bgxx_page_list = value_dict['bgxx_page_list']
#     for page in bgxx_page_list:
#         url = '{}{}'.format(host, value_dict['uri_dict']['bgxx_uri'])
#         data = {
#             "draw": page,
#             "start": (page - 1) * 5,
#             "length": 5
#         }
#         resp = send_request('post', url, data=data)
#         page_dict['bgxx'].append({
#             'page': page,
#             'html': resp.text
#         })
#
#
# # 分支机构页码
# def init_fzjg_page():
#     url = '{}{}'.format(host, value_dict['uri_dict']['fzjg_uri'])
#     resp = send_request('get', url)
#     value_dict['fzjg_page_list'] = get_total_page(resp.text)
#
#
# def iter_fzjg_list():
#     page_dict['fzjg'] = []
#     for page in value_dict['fzjg_page_list']:
#         url = '{}{}?start={}'.format(host, value_dict['uri_dict']['fzjg_uri'], (page - 1) * 9)
#         resp = send_request('get', url)
#         page_dict['fzjg'].append({
#             'page': page,
#             'html': resp.text
#         })
#
#
# # 动产抵押
# def init_dcdy_page():
#     url = '{}{}'.format(host, value_dict['uri_dict']['dcdy_uri'])
#     data = {
#         "draw": 1,
#         "start": 0,
#         "length": 5
#     }
#     resp = send_request('post', url, data=data)
#     value_dict['dcdy_page_list'] = get_total_page(resp.text)
#

# def iter_dcdy_list():
#     page_dict['dcdy'] = []
#     value_dict['dcdyxq_id_list'] = []
#     url = '{}{}'.format(host, value_dict['uri_dict']['dcdy_uri'])
#
#     def get_dcdy_params(html):
#         try:
#             data_list = json.loads(html).get('data', [])
#             for item in data_list:
#                 mor_reg_id = item.get('morReg_Id')
#                 if item.get('type') in ['1', '2'] and mor_reg_id and mor_reg_id not in value_dict['dcdyxq_id_list']:
#                     value_dict['dcdyxq_id_list'].append(mor_reg_id)
#         except Exception as e:
#             logger.warning(u'下载动产抵押页面数据格式不正确 {}'.format(str(e)))
#
#     dcdy_page_list = value_dict['dcdy_page_list']
#     for page in dcdy_page_list:
#         data = {
#             "draw": page,
#             "start": (page - 1) * 5,
#             "length": 5
#         }
#         resp = send_request('post', url, data=data)
#         get_dcdy_params(resp.text)
#         page_dict['dcdy'].append({
#             'page':page,
#             'html': resp.text
#         })
#
#
# def iter_dcdyxq_list():
#     page_dict['dcdy_xq_list'] = []
#     for dcdyxq_id in value_dict['dcdyxq_id_list']:
#         dcdy_xq_key_list = [
#             'mortregpersoninfo',
#             'mortCreditorRightInfo',
#             'mortGuaranteeInfo',
#             'getMortAltItemInfo',
#             'getMortRegCancelInfo'
#         ]
#         for xq_key in dcdy_xq_key_list:
#             xq_url = '{}/corp-query-entprise-info-{}-{}.html'.format(host, xq_key, dcdyxq_id)
#             resp = send_request('get', xq_url)
#             page_dict['dcdy_xq_list'].append({
#                 'html': resp.text,
#                 'id': dcdyxq_id,
#                 'xq_key': xq_key,
#             })
#             time.sleep(2)

#
# def init_gqcz_page():
#     url = '{}{}'.format(host, value_dict['uri_dict']['gqcz_uri'])
#     data = {
#         "draw": 1,
#         "start": 0,
#         "length": 5
#     }
#     resp = send_request('post', url, data=data)
#     value_dict['gqcz_page_list'] = get_total_page(resp.text)
#
#
# def iter_gqcz_page():
#     page_dict['gqcz'] = []
#     gqcz_page_list = value_dict['gqcz_page_list']
#     url = '{}{}'.format(host, value_dict['uri_dict']['gqcz_uri'])
#     for page in gqcz_page_list:
#         data = {
#             "draw": page,
#             "start": (page - 1) * 5,
#             "length": 5
#         }
#
#         resp = send_request('post', url, data=data)
#         page_dict['gqcz'].append({
#             'page': page,
#             'html': resp.text
#         })
#
#
# def init_sfxz_page():
#     url = '{}{}'.format(host, value_dict['uri_dict']['sfxz_uri'])
#     data = {
#         "draw": 1,
#         "start": 0,
#         "length": 5
#     }
#     resp = send_request('post', url, data=data)
#     value_dict['sfxz_page_list'] = get_total_page(resp.text)
#
#
# def iter_sfxz_page():
#     page_dict['sfxz'] = []
#     sfxz_page_list = value_dict['sfxz_page_list']
#     url = '{}{}'.format(host, value_dict['uri_dict']['gqcz_uri'])
#     for page in sfxz_page_list:
#         data = {
#             "draw": page,
#             "start": (page - 1) * 5,
#             "length": 5
#         }
#
#         resp = send_request('post', url, data=data)
#         page_dict['sfxz'].append({
#             'page': page,
#             'html': resp.text
#         })
#

from settings import default_settings
from utils import get_ics_logger
from utils.db import CdrcbDb
logger = get_ics_logger('xxx')
if __name__ == '__main__':
    mysql_db = CdrcbDb(default_settings.MYSQL_TASK_DATA_DB, logger)
    logger.info('mysql_db_id: {}'.format(mysql_db))
    update_pattern = 'UPDATE seedss SET status={} WHERE task_id = "{}";'.format(0, '1111111111')
    mysql_db.execSql(update_pattern)

