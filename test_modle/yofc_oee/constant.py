# filename = ""
# 文件名拼接路径
filename_path = "./raw_data/{}"

# raw_data文件夹路径
raw_data_path = "./raw_data"

# get_oee()中传的文件名 判断格式的正则    WH_Y2018W44_SH.xls
judge_filename_re = r"^[A-Z]{2}_Y[0-9]{4}W[0-9]{1,2}_[A-Z]{2}\.xls$"

# 四地光缆OEE记录.xlsx
four_area_oee_xlsx = "./overview_oee/四地光缆OEE记录.xlsx"

# 四地光缆OEE记录.csv
four_area_oee_csv = "./overview_oee/四地光缆OEE记录.csv"

# 中间数据csv文件位置
export_data_path = "./export_data/"
# y轴week最大值
week = 51




tot_pro_columns = ['wuhan', 'lanzhou', 'shenyang', 'yinni']

# figure line 和 figure select line的尺寸
plot_width = 900
plot_height = 350
tools = "pan,wheel_zoom,box_zoom,reset,tap,hover,save"
title = "各基地每周oee指标趋势图"
y_range = [0, 1.2]

hover_tooltips_1 = '周数'
hover_tooltips_2 = '武汉（'
hover_tooltips_3 = '兰州（'
hover_tooltips_4 = '沈阳（'
hover_tooltips_5 = '印尼（'

line_width = 2

legend_1 = '武汉（'
legend_2 = '兰州（'
legend_3 = '沈阳（'
legend_4 = '印尼（'

wh_color = "#DD5246"
lz_color = "#4A8AF4"
sy_color = "#FFCD42"
yn_color = "#1AA15F"

legend_location = "top_left"
legend_orientation = "horizontal"

xgrid_grid_line_color = "navy"
xgrid_grid_line_alpha = 0.1
xgrid_minor_grid_line_color = "navy"
xgrid_minor_grid_line_alpha = 0.3

# logo
logo_url = "https://raw.githubusercontent.com/Mrwang19960102/public_images/master/shuge.png"