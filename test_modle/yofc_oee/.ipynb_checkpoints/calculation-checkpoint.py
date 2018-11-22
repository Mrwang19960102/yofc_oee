import numpy as np
import pandas as pd
import os
import warnings
from pandas import DataFrame
import re
from cable_oee import constant

warnings.filterwarnings('ignore')


class OEE(object):
    def __init__(self):
        self.filename_path = constant.filename_path
        self.filename = ""
        self.place = ""
        self.year = ""
        self.week = ""
        self.pro = ""
        self.info_list = list()
        self.week_set = set()
        self.place_set = set()
        self.year_set = set()
        self.pro_set = set()

    def get_info(self):
        """解析文件名　获取信息"""
        self.place = self.filename[-18:-16]
        self.year = self.filename[-14:-10]
        self.week = self.filename[-9:-7]
        self.pro = self.filename[-6:-4]
        self.info_list = [self.place, self.year, self.week, self.pro, self.filename]

    def create_csv(self, pub_oee,file):
        # file = self.info_list[0] + "_Y" + self.info_list[1] + "W" + self.info_list[2] + "_" + self.info_list[
        #     3] + "_OEE.csv"
        path = constant.export_data_path + self.info_list[0]
        if not os.path.exists(path):
            os.makedirs(path)
        pub_oee.to_csv(path + "/" + file, encoding="utf_8_sig")
        print("{}第{}周的{}工序的oee指标值csv文件已经生成,文件名为{},在data_export文件夹下的{}文件夹中".format(self.info_list[0],
                                                                                  self.info_list[2], self.info_list[3],
                                                                                  file, self.info_list[0]))

    def group_and_oee(self, read_data):
        """得到每个生产商每周oee数据、生成oee数据的csv文件"""
        filename = self.info_list[0] + "_Y" + self.info_list[1] + "W" + self.info_list[2] + "_" + self.info_list[
            3] + "_OEE_data.csv"
        self.create_csv(read_data[['设备', 'date', '班次', '有效工时', 'wt_fix']],filename)
        pub_oee = read_data[['设备', 'date', '班次', 'wt_fix']].groupby(['设备', 'date', '班次']).sum()
        pub_oee['oee'] = pub_oee['wt_fix'] / 720

        group_filename = self.info_list[0] + "_Y" + self.info_list[1] + "W" + self.info_list[2] + "_" + self.info_list[
            3] + "_OEE_group.csv"
        self.create_csv(pub_oee,group_filename)
        public_oee_st = pub_oee[pub_oee['oee'] <= 1]['oee'].mean()
        return public_oee_st

    def get_is_coiling(self, st_data):
        """输入`data_frame`判断是否上盘，追加列"""
        st_data['SN'] = st_data['流水号'].str.slice(0, 12)
        st_data['SN-'] = st_data['SN'].shift(periods=1)
        st_data['设备-'] = st_data['设备'].shift(periods=1)
        data_frame = st_data.reset_index()
        data_frame = data_frame.drop(['index'], axis=1)

        data_frame['change_SN'] = (data_frame['SN'] != data_frame['SN-'])
        data_frame['same_facility'] = (data_frame['设备'] == data_frame['设备-'])
        data_frame['is_coiling'] = (data_frame['change_SN'] == data_frame['same_facility'])
        data_frame['is_coiling2'] = data_frame['is_coiling']
        return data_frame

    def calculate_CL_oee(self):
        """CL工序"""
        cl_data = pd.read_excel(self.filename, 'Sheet')
        cl_data['date'] = cl_data['生产日期'].dt.strftime('%Y-%m-%d')
        cl_data['wt_fix'] = cl_data['有效工时'] + np.greater(cl_data['有效工时'], 0) * 4
        oee_cl = self.group_and_oee(cl_data)
        return oee_cl

    def calculate_SC_oee(self):
        """SC工序"""
        sc_data = pd.read_excel(self.filename, 'Sheet')
        sc_data['date'] = sc_data['生产日期'].dt.strftime('%Y-%m-%d')

        sc_data['光纤上盘'] = sc_data['套管芯数']
        sc_data['sign'] = (((sc_data['光纤上盘']) <= 6) * 2.3) + (
            (((sc_data['光纤上盘']) <= 12) & ((sc_data['光纤上盘']) > 6)) * 1.7) \
                          + (((sc_data['光纤上盘']) > 12) * 1.3)
        sc_data = sc_data[sc_data['有效工时'] > 0]
        # 修正工时 = 有效工时+上盘时间  上盘时间=光纤上盘*sign  光纤上盘=套管芯数
        sc_data['wt_fix'] = sc_data['有效工时'] + (sc_data['套管芯数'] * sc_data['sign'])
        oee_sc = self.group_and_oee(sc_data)
        return oee_sc

    def calculate_ST_oee(self):
        """ST工序"""
        st_data = pd.read_excel(self.filename, 'Sheet')
        st_data = st_data.sort_values(by=['设备', '生产日期'])
        st_data['date'] = st_data['生产日期'].dt.strftime('%Y-%m-%d')
        st_data = self.get_is_coiling(st_data)

        st_data['coiling_fix'] = st_data['is_coiling2'] * (st_data['缆芯单元数'] + 6)
        st_data['wt_valid'] = st_data['有效工时'] > 0
        st_data['wt_fix'] = st_data['wt_valid'] * (st_data['有效工时'] + st_data['coiling_fix'] + 5 + 10)

        # 生成csv文件 计算得到oee数据
        oee_st = self.group_and_oee(st_data)
        return oee_st

    def calculate_SH_oee(self):
        """SH工序"""
        # 读取excel文件，数据预处理
        sh_data = pd.read_excel(self.filename, sheet_name='Sheet')
        # df = sh_data[['设备', '生产日期', '班次', '班组', '光缆型号', '流水号', '有效工时']]
        sh_data = sh_data.sort_values(by=['设备', '生产日期'])
        # 加工修正工时用数据
        sh_data['date'] = sh_data['生产日期'].dt.strftime("%Y-%m-%d")
        sh_data = self.get_is_coiling(sh_data)
        sh_data['8_time_fix'] = (sh_data['光缆型号'].str.contains('C8', regex=False)) * 10
        sh_data['wiring_time_fix'] = sh_data['is_coiling2'] * 9.5
        # 计算oee数据
        sh_data['wt_valid'] = sh_data['有效工时'] > 0
        sh_data['wt_fix'] = sh_data['wt_valid'] * (
            sh_data['有效工时'] + sh_data['wiring_time_fix'] + 8.3 + sh_data['8_time_fix'])
        oee_sh = self.group_and_oee(sh_data)
        return oee_sh

    def confirm_place_pro(self, place, pro):
        """确认生产产地和工序"""
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

    def update_oee(self, oee_data):
        df = pd.read_excel(constant.four_area_oee_xlsx)
        colum = "Unnamed: " + str(int(self.week) + 2)
        place_pro = self.confirm_place_pro(self.place, self.pro)
        a = df[df['Unnamed: 2'] == place_pro].index
        df.loc[a, colum] = float(oee_data)
        # df.to_excel("./四地光缆OEE记录2.xlsx",encoding="utf_8_sig")
        DataFrame(df).to_excel(constant.four_area_oee_xlsx, sheet_name='OEE记录表', index=False, header=True)
        excel_df = pd.read_excel(constant.four_area_oee_xlsx, encoding='utf-8', header=2)
        # df.head(16)
        excel_df.to_csv(constant.four_area_oee_csv, encoding="utf_8_sig")
        f = open(constant.four_area_oee_csv, encoding='utf-8')
        csv_df = pd.read_csv(f)
        print("数据已成功写入四地光缆OEE记录表，在overview_oee文件夹下")
        print("-" * 50)

    def determine_pro(self):
        """判断工序　得到oee数值"""
        if self.pro == "CL":
            oee_data = self.calculate_CL_oee()
        elif self.pro == "SC":
            oee_data = self.calculate_SC_oee()
        elif self.pro == "ST":
            oee_data = self.calculate_ST_oee()
        elif self.pro == "SH":
            oee_data = self.calculate_SH_oee()
        # print(oee_data)
        print("%s%s年第%s周%s工序oee数据为%s" % (self.place, self.year, self.week, self.pro, oee_data))
        return oee_data

    def calculate(self):
        """计算oee数值"""
        # 得到文件名信息
        self.get_info()
        # 得到oee数值
        oee_data = self.determine_pro()
        # 将oee数据写入四地光缆表
        self.update_oee(oee_data)

    @staticmethod
    def print_reminders():
        """文件输入格式错误输出提示信息"""
        print("-" * 50)
        print("输入错误，正确格式为：")
        print("例 计算单文件的oee值： 'WH_Y2018W44_SH.xls' ")
        print("例 计算多个文件的oee值： ['WH_Y2018W44_SH.xls', 'WH_Y2018W44_ST.xls', 'WH_Y2018W44_CL.xls'] ")
        print("-" * 50)

    def file_name_reminders(self, filename):
        """文件命名错误提示信息"""
        print("-" * 50)
        print("{}文件命名格式错误， 正确格式为：".format(filename))
        print("前两位为制造基地缩写的大写字母_Y年份W周_工序缩写的大写字母.xls")
        print("例 'WH_Y2018W45_SH.xls'　＝> 武汉2018年45周护套产值表")
        print("-" * 50)

    def judge_exist(self):
        """raw_data中所有文件以及地区、年、周、工序集合"""
        # week_list = []
        path = constant.raw_data_path
        for dirpath, dirnames, filenames in os.walk(path):
            for each in filenames:
                self.week_set.add(each[9:11])
                self.year_set.add(each[4:8])
                self.place_set.add(each[0:2])
                self.pro_set.add(each[-6:-4])

    def judge_filename(self, filename):
        """判断文件名命名是否正确"""
        # 文件名必须符合正则，文件名中的地区、年、周、工序必须在raw_data里
        self.judge_exist()
        if re.match(constant.judge_filename_re, filename):
            if (filename[0:2] in self.place_set) and (filename[4:8] in self.year_set) and \
                    (filename[9:11] in self.week_set) and (filename[-6:-4] in self.pro_set):
                return True
        else:
            return False

    def calculate_oee(self, filename_list):
        """得到oee"""
        # 判断是否是单个文件
        if isinstance(filename_list, str):
            # 判断文件命名格式
            if self.judge_filename(filename_list):
                self.filename = self.filename_path.format(filename_list)
                self.calculate()
            else:
                self.file_name_reminders(filename_list)

        # 判断是否是文件列表
        elif isinstance(filename_list, list):
            for each in filename_list:
                # 判断文件命名格式
                if self.judge_filename(each):
                    self.filename = self.filename_path.format(each)
                    self.calculate()
                else:
                    self.file_name_reminders(each)
        # 都不是
        else:
            self.print_reminders()


# if __name__ == '__main__':
oee = OEE()
#     oee.calculate_oee(["WH_Y2018W44_ST.xls", "WH_Y2018W49_ST.xls", "WH_Y2018W45_ST.xls"])
    # with open("constant_oee.py", "w") as f:
    #     f.write("\roee_num={}".format(str(oee_num)))
    # oee.judge_exist()
    # oee.judge_filename("WH_Y2018W45_ST.xls")
