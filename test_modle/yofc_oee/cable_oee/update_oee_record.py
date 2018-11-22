from cable_oee.calculation import calculate_oee, get_info

import numpy as np
import pandas as pd
from pandas import DataFrame


def update_oee(filename,oee_data):
    info_list = get_info(filename)
    place = info_list[0]
    week = info_list[2]
    pro = info_list[3]

    df = pd.read_excel("./overview_oee/四地光缆OEE记录.xlsx")
    colum = "Unnamed: " + str(int(week) + 2)
    place_pro = confirm_place_pro(place, pro)
    a = df[df['Unnamed: 2'] == place_pro].index
    df.loc[a, colum] = float(oee_data)
    # df.to_excel("./四地光缆OEE记录2.xlsx",encoding="utf_8_sig")
    DataFrame(df).to_excel('./overview_oee/四地光缆OEE记录.xlsx', sheet_name='OEE记录表', index=False, header=True)
    excel_df = pd.read_excel("./overview_oee/四地光缆OEE记录.xlsx", encoding='utf-8', header=2)
    # df.head(16)
    excel_df.to_csv('./overview_oee/四地光缆OEE记录.csv', encoding="utf_8_sig")
    f = open('./overview_oee/四地光缆OEE记录.csv', encoding='utf-8')
    csv_df = pd.read_csv(f)
    print("数据已成功写入")
#     return csv_df


def confirm_place_pro(place, pro):
    """
    确认生产产地和工序
    :param place: 生产产地
    :param pro: 生产工序
    :return:
    """
    if place == "WH":
        if pro == "CL":
            return "武汉着色（CL）"
        elif pro == "SC":
            return "武汉二套（SC）"
        elif pro == "ST":
            return "武汉成缆（ST）"
        elif pro == "SH":
            return "武汉护套（SH）"
    elif place == "LZ":
        if pro == "CL":
            return "兰州着色（CL）"
        elif pro == "SC":
            return "兰州二套（SC）"
        elif pro == "ST":
            return "兰州成缆（ST）"
        elif pro == "SH":
            return "兰州护套（SH）"
    elif place == "SY":
        if pro == "CL":
            return "沈阳着色（CL）"
        elif pro == "SC":
            return "沈阳二套（SC）"
        elif pro == "ST":
            return "沈阳成缆（ST）"
        elif pro == "SH":
            return "沈阳护套（SH）"

    elif place == "YN":
        if pro == "CL":
            return "印尼着色（CL）"
        elif pro == "SC":
            return "印尼二套（SC）"
        elif pro == "ST":
            return "印尼成缆（ST）"
        elif pro == "SH":
            return "印尼护套（SH）"


# updata_oee()
