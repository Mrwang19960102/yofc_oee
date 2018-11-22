import numpy as np
import pandas as pd
import os

import warnings

warnings.filterwarnings('ignore')


def calculate_CL_oee(excel_file_cl, info_list):
    """
    计算着色（CL）的oee
    """
    # 读取excel文件，设置时间格式  选取有助于修正后有效工时计算的字段 排序之后重新设置索引。
    cl_data = pd.read_excel(excel_file_cl, 'Sheet')
    cl_data['date'] = cl_data['生产日期'].dt.strftime('%Y-%m-%d')
    cl_data['wt_fix'] = cl_data['有效工时'] + np.greater(cl_data['有效工时'], 0) * 4
    
    oee_cl = group_and_oee(cl_data, info_list)
    return oee_cl


def calculate_SC_oee(excel_file_sc, info_list):
    """
    :param excel_file: 数据源文件
    :return: sc计算的oee
    """
    # 读取excel文件，设置时间格式  选取有助于修正后有效工时计算的字段。
    sc_data = pd.read_excel(excel_file_sc, 'Sheet')
    sc_data['date'] = sc_data['生产日期'].dt.strftime('%Y-%m-%d')

    sc_data['光纤上盘'] = sc_data['套管芯数']
    sc_data['sign'] = (((sc_data['光纤上盘']) <= 6) * 2.3) + ((((sc_data['光纤上盘']) <= 12) & ((sc_data['光纤上盘']) > 6)) * 1.7) \
                      + (((sc_data['光纤上盘']) > 12) * 1.3)
    sc_data = sc_data[sc_data['有效工时'] > 0]
    # 修正工时 = 有效工时+上盘时间  上盘时间=光纤上盘*sign  光纤上盘=套管芯数
    sc_data['wt_fix'] = sc_data['有效工时'] + (sc_data['套管芯数'] * sc_data['sign'])

    oee_sc = group_and_oee(sc_data, info_list)

    return oee_sc


def calculate_ST_oee(excel_file_st, info_list):
    """
    计算st成缆oee数据
    :param excel_file_st: st数据源文件
    :return: st成缆oee数据
    """
    # 读取excel文件，设置时间格式
    st_data = pd.read_excel(excel_file_st, 'Sheet')
    st_data = st_data.sort_values(by=['设备', '生产日期'])
    st_data['date'] = st_data['生产日期'].dt.strftime('%Y-%m-%d')
    st_data = get_is_coiling(st_data)

    st_data['coiling_fix'] = st_data['is_coiling2'] * (st_data['缆芯单元数'] + 6)
    st_data['wt_valid'] = st_data['有效工时'] > 0
    st_data['wt_fix'] = st_data['wt_valid'] * (st_data['有效工时'] + st_data['coiling_fix'] + 5 + 10)

    # 生成csv文件 计算得到oee数据
    oee_st = group_and_oee(st_data, info_list)
    return oee_st


def calculate_SH_oee(excel_file_sh, info_list):
    """
    计算sh护套oee数据
    :param excel_file_sh: sh数据源文件
    :return: sh护套oee数据
    """
    # 读取excel文件，数据预处理
    sh_data = pd.read_excel(excel_file_sh, sheet_name='Sheet')
    # df = sh_data[['设备', '生产日期', '班次', '班组', '光缆型号', '流水号', '有效工时']]
    sh_data = sh_data.sort_values(by=['设备', '生产日期'])

    # 加工修正工时用数据
    sh_data['date'] = sh_data['生产日期'].dt.strftime("%Y-%m-%d")
    sh_data = get_is_coiling(sh_data)
    # df = df.reset_index()
    # df = df.drop(['index'], axis=1)
    sh_data['8_time_fix'] = (sh_data['光缆型号'].str.contains('C8', regex=False)) * 10

    sh_data['wiring_time_fix'] = sh_data['is_coiling2'] * 9.5

    # 计算oee数据
    sh_data['wt_valid'] = sh_data['有效工时'] > 0
    sh_data['wt_fix'] = sh_data['wt_valid'] * (sh_data['有效工时'] + sh_data['wiring_time_fix'] + 8.3 + sh_data['8_time_fix'])
    oee_sh = group_and_oee(sh_data, info_list)
    return oee_sh




def get_is_coiling(data_new):
    """

    :return:
    """
    data_new['SN'] = data_new['流水号'].str.slice(0, 13)
    data_new['SN-'] = data_new['SN'].shift(periods=1)
    data_new['设备-'] = data_new['设备'].shift(periods=1)
    data_new = data_new.reset_index()
    data_new = data_new.drop(['index'], axis=1)

    data_new['change_SN'] = (data_new['SN'] != data_new['SN-'])
    data_new['same_facility'] = (data_new['设备'] == data_new['设备-'])
    data_new['is_coiling'] = (data_new['change_SN'] == data_new['same_facility'])
    data_new['is_coiling2'] = data_new['is_coiling']
    return data_new


def group_and_oee(read_data, info_list):
    """
    得到每个生产商每周oee数据、生成oee数据的csv文件
    :param read_data: 读取的excel文件
    :return: oee
    """
    # place = info_list[0]
    # year = info_list[1]
    # week = info_list[2]
    # pro = info_list[3]
#     create_csv(info_list, pub_oee)
    filename = info_list[0] + "_Y" + info_list[1] + "W" + info_list[2] + "_" + info_list[3] + "_OEE_data.csv"
    create_csv(filename,info_list, read_data[['设备','date','班次','有效工时','wt_fix']])
    pub_oee = read_data[['设备', 'date', '班次', 'wt_fix']].groupby(['设备', 'date', '班次']).sum()
    pub_oee['oee'] = pub_oee['wt_fix'] / 720

    # print(info_list)
    filename = info_list[0] + "_Y" + info_list[1] + "W" + info_list[2] + "_" + info_list[3] + "_OEE_group.csv"
    create_csv(filename,info_list, pub_oee)
    public_oee_st = pub_oee[pub_oee['oee'] <= 1]['oee'].mean()
    return public_oee_st


def create_csv(filename,info_list, public_oee):
    """
    生成对应的oee数据csv文件
    :param info_list:
    :return:
    """
    print(filename)
    path = "./data_export/" + info_list[0]
    if not os.path.exists(path):
        os.makedirs(path)
    public_oee.to_csv(path + "/" + filename, encoding="utf_8_sig")
    print("oee指标值csv文件已经生成")


def tot_oee():
    oee_cl = calculate_CL_oee("./raw_data/WH_Y2018W46_CL.xls", ['WH', '2018', '46', 'CL'])
    oee_sc = calculate_SC_oee("./raw_data/WH_Y2018W46_SC.xls", ['WH', '2018', '46', 'SC'])
    oee_st = calculate_ST_oee("./raw_data/WH_Y2018W46_ST.xls", ['WH', '2018', '46', 'ST'])
    oee_sh = calculate_SH_oee("./raw_data/WH_Y2018W46_SH.xls", ['WH', '2018', '46', 'SH'])
    oee = pd.Series(data=[oee_cl, oee_sc, oee_st, oee_sh], index=['CL', 'SC', 'ST', 'SH'])
    print(oee)

def get_info(filename):
    """
    解析文件名，获取信息
    :param file_name: 文件名
    :return: 信息列表
    """
    info_list = []
    #     filename = "WH_Y2018W43_ST.xls"
    place = filename[-18:-16]
    year = filename[-14:-10]
    week = filename[-9:-7]
    pro = filename[-6:-4]
    info_list.append(place)
    info_list.append(year)
    info_list.append(week)
    info_list.append(pro)
    info_list.append(filename)
    return info_list


def calculate_oee(filename):
    """

    :param info_list:
    :return:
    """
    info_list = get_info(filename)
    place = info_list[0]
    year = info_list[1]
    week = info_list[2]
    pro = info_list[3]
    if pro == "CL":
        oee_data = calculate_CL_oee(filename, info_list)
    elif pro == "SC":
        oee_data = calculate_SC_oee(filename, info_list)
    elif pro == "ST":
        oee_data = calculate_ST_oee(filename, info_list)
    elif pro == "SH":
        oee_data = calculate_SH_oee(filename, info_list)
    print("%s基地%s年第%s周%s工序oee数据：%s" % (place, year, week, pro, oee_data))
    return oee_data

# if __name__ == '__main__':
#     get_oee()

