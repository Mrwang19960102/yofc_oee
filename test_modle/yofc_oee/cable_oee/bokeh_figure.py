import numpy as np
import pandas as pd
import os

from bokeh.io import show, output_notebook, output_file

output_notebook()
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, TapTool, Patches, RangeTool, FactorRange, Range1d, ImageURL
from bokeh.transform import factor_cmap
from bokeh.layouts import column
from bokeh.models.glyphs import ImageURL
from bokeh.models import NumeralTickFormatter
from bokeh.models.widgets import Panel, Tabs

week_list2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
              11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
              21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
              31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
              41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

def makir_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def filtrate_data():
    df = pd.read_csv("./overview_oee/四地光缆OEE记录.csv")
    df = df[0:16].drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)

    wh_cl = df[0:1].transpose()
    lz_cl = df[4:5].transpose()
    sy_cl = df[8:9].transpose()
    yn_cl = df[12:13].transpose()
    tot_cl = wh_cl.join(lz_cl).join(sy_cl).join(yn_cl)
    tot_cl.columns = ['wuhan', 'lanzhou', 'shenyang', 'yinni']
    df_CL = tot_cl.drop(['Unnamed: 2'])

    wh_sc = df[1:2].transpose()
    lz_sc = df[5:6].transpose()
    sy_sc = df[9:10].transpose()
    yn_sc = df[13:14].transpose()
    tot_sc = wh_sc.join(lz_sc).join(sy_sc).join(yn_sc)
    tot_sc.columns = ['wuhan', 'lanzhou', 'shenyang', 'yinni']
    df_SC = tot_sc.drop(['Unnamed: 2'])

    wh_st = df[2:3].transpose()
    lz_st = df[6:7].transpose()
    sy_st = df[10:11].transpose()
    yn_st = df[14:15].transpose()
    tot_st = wh_st.join(lz_st).join(sy_st).join(yn_st)
    tot_st.columns = ['wuhan', 'lanzhou', 'shenyang', 'yinni']
    df_ST = tot_st.drop(['Unnamed: 2'])

    wh_sh = df[3:4].transpose()
    lz_sh = df[7:8].transpose()
    sy_sh = df[11:12].transpose()
    yn_sh = df[15:16].transpose()
    tot_sh = wh_sh.join(lz_sh).join(sy_sh).join(yn_sh)
    tot_sh.columns = ['wuhan', 'lanzhou', 'shenyang', 'yinni']
    df_SH = tot_sh.drop(['Unnamed: 2'])

    return df_CL, df_SC, df_ST, df_SH


def add_map(df, pro):
    """
    由数据得到绘图figure对象
    :param df:筛选得到某工序的dataframe对象
    :param pro:生产工序
    :return:返回figure对象
    """
    html_file = "./HTML/各基地每周oee指标趋势图.html"
    pather_path = "./HTML"
    makir_path(pather_path)
    output_file(html_file)
    data = {
        'y1': df['wuhan'],
        'y2': df['lanzhou'],
        'y3': df['shenyang'],
        'y4': df['yinni'],
        'x': week_list2
    }
    colors=["#DD5246","#4A8AF4","#FFCD42","#1AA15F"]
    circle_fill_color = "white"
    source = ColumnDataSource(data=data)
    p = figure(plot_width=900, plot_height=350, tools="pan,wheel_zoom,box_zoom,reset,tap,hover,save",
               title="各基地每周oee指标趋势图" + "("+pro+")" , y_range=[0, 1.2])
    p.hover.tooltips = [('周数', "@x"), ('武汉（' + pro + '）', "@y1"), ('兰州（' + pro + '）', "@y2"),
                        ('沈阳（' + pro + '）', "@y3"), ('印尼（' + pro + '）', "@y4")]
    p.line('x', 'y1', line_width=2, legend='武汉（' + pro + '）', color=colors[0], source=source)
    p.line('x', 'y2', line_width=2, legend='兰州（' + pro + '）', color=colors[1], source=source)
    p.line('x', 'y3', line_width=2, legend='沈阳（' + pro + '）', color=colors[2], source=source)
    p.line('x', 'y4', line_width=2, legend='印尼（' + pro + '）', color=colors[3], source=source)
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.xgrid.grid_line_color = "gray"
    p.xgrid.grid_line_alpha = 0.1
    p.xgrid.minor_grid_line_color = 'gray'
    p.xgrid.minor_grid_line_alpha = 0.3
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    p.y_range.start = 0
    p.toolbar.logo = None
    
    # 绘制折点
    p.circle(x=data['x'], y=data['y1'], size=6, color=colors[0], alpha=0.8, fill_color=circle_fill_color)
    p.circle(x=data['x'], y=data['y2'], size=6, color=colors[1], alpha=0.8, fill_color=circle_fill_color)
    p.circle(x=data['x'], y=data['y3'], size=6, color=colors[2], alpha=0.8, fill_color=circle_fill_color)
    p.circle(x=data['x'], y=data['y4'], size=6, color=colors[3], alpha=0.8, fill_color=circle_fill_color)

    return p, source, pro


def add_select_map(df, pro):
    """
    由数据得到绘图figure对象
    :param df:筛选得到某工序的dataframe对象
    :param pro:生产工序
    :return:返回figure对象
    """
    html_file = "./HTML/各基地每周oee指标趋势图（范围选择）.html"
    pather_path = "./HTML"
    makir_path(pather_path)
    output_file(html_file)
    data = {
        'y1': df['wuhan'],
        'y2': df['lanzhou'],
        'y3': df['shenyang'],
        'y4': df['yinni'],
        'x': week_list2
    }
    source = ColumnDataSource(data=data)
    colors=["#DD5246","#4A8AF4","#FFCD42","#1AA15F"]
    circle_fill_color = "white"
    p = figure(plot_width=900, plot_height=350, tools="pan,wheel_zoom,box_zoom,reset,tap,hover",
               title="各基地每周oee指标趋势图" + "("+pro+")" , y_range=[0, 1.2], x_range=(week_list2[20], week_list2[30]))
    p.hover.tooltips = [('周数', "@x"), ('武汉（' + pro + '）', "@y1"), ('兰州（' + pro + '）', "@y2"),
                        ('沈阳（' + pro + '）', "@y3"), ('印尼（' + pro + '）', "@y4")]
    p.line('x', 'y1', line_width=2, legend='武汉（' + pro + '）', color=colors[0], source=source)
    p.line('x', 'y2', line_width=2, legend='兰州（' + pro + '）', color=colors[1], source=source)
    p.line('x', 'y3', line_width=2, legend='沈阳（' + pro + '）', color=colors[2], source=source)
    p.line('x', 'y4', line_width=2, legend='印尼（' + pro + '）', color=colors[3], source=source)
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.xgrid.grid_line_color = "gray"
    p.xgrid.grid_line_alpha = 0.1
    p.xgrid.minor_grid_line_color = 'gray'
    p.xgrid.minor_grid_line_alpha = 0.3
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    p.y_range.start = 0
    p.toolbar.logo = None
    # 绘制折点
    p.circle(x=data['x'], y=data['y1'], size=8, color=colors[0], alpha=1, fill_color=circle_fill_color)
    p.circle(x=data['x'], y=data['y2'], size=8, color=colors[1], alpha=1, fill_color=circle_fill_color)
    p.circle(x=data['x'], y=data['y3'], size=8, color=colors[2], alpha=1, fill_color=circle_fill_color)
    p.circle(x=data['x'], y=data['y4'], size=8, color=colors[3], alpha=1, fill_color=circle_fill_color)

    return p, source, pro




def add_select(p, source, pro):
    select = figure(title="各基地每周oee指标趋势图" + "("+pro+")", plot_height=200, plot_width=900, y_range=p.y_range,
                    tools="pan,wheel_zoom,box_zoom,reset,tap,hover", toolbar_location=None,
                    background_fill_color="#efefef")
    range_rool = RangeTool(x_range=p.x_range)
    range_rool.overlay.fill_color = "navy"
    range_rool.overlay.fill_alpha = 0.2

    select.line('x', 'y1', color="#DD5246", source=source)
    select.line('x', 'y2', color="#4A8AF4", source=source)
    select.line('x', 'y3', color="#FFCD42", source=source)
    select.line('x', 'y4', color="#1AA15F", source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_rool)
    select.toolbar.active_multi = range_rool
    select.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    select.xgrid.grid_line_color = "gray"
    select.xgrid.grid_line_alpha = 0.1
    select.xgrid.minor_grid_line_color = 'gray'
    select.xgrid.minor_grid_line_alpha = 0.3
    
    return select


def add_logo(p):
    """
    增加logo
    """
    url = "https://raw.githubusercontent.com/Mrwang19960102/public_images/master/shuge.png"
    # anchor="bottom_right", 
    width = 48 
    height = 1.2
    img = p.image_url(url=dict(value=url), x=width-6, y=0.18, w=80, h=20, w_units='screen', h_units='screen',
                      global_alpha=0.5)
    p.extra_x_ranges["x_screen"] = Range1d(0, width, bounds="auto")
    p.extra_y_ranges["y_screen"] = Range1d(0, height, bounds="auto")

    img.x_range_name = "x_screen"
    img.y_range_name = "y_screen"

def map_select_logo(df, pro):
    p, source, pro = add_select_map(df, pro)
    select = add_select(p, source, pro)
    add_logo(p)
    add_logo(select)
    P = column(p, select)
    tab = Panel(child=P, title=pro)
    return tab


def draw_chart_selection():
    df_CL, df_SC, df_ST, df_SH = filtrate_data()
    tab1 = map_select_logo(df_CL, "CL")
    tab2 = map_select_logo(df_SC, "SC")
    tab3 = map_select_logo(df_ST, "ST")
    tab4 = map_select_logo(df_SH, "SH")
    tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])
    
    show(tabs)


def map_logo(df, pro):
    """
    增加logo，添加p对象至tab为的子对象
    :param df: 筛选得到某工序的dataframe对象
    :param pro: 生产工序
    :return:
    """
    p, source, pro = add_map(df, pro)
#     add_logo(p)
    tab = Panel(child=p, title=pro)
    return tab



def draw_chart_line():
    """
    绘制折线图
    :return:
    """
    df_CL, df_SC, df_ST, df_SH = filtrate_data()

    tab1 = map_logo(df_CL, 'CL')
    tab2 = map_logo(df_SC, 'SC')
    tab3 = map_logo(df_ST, 'ST')
    tab4 = map_logo(df_SH, 'SH')

    tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])
    show(tabs)




def figure_vbar():
    df_SH = filtrate_data()
    TOOLS = "pan,wheel_zoom,box_zoom,reset,tap,hover,save"
    week_num = list(df_SH.index)
    pro_place = ['W', 'L', 'S', 'Y']
    a = 1
    place = []
    while a <= 50:
        place.append("W")
        place.append("L")
        place.append("S")
        place.append("Y")
        a += 1
    data = {
        'week_num': df_SH.index,
        'wuhan_sh': df_SH['wuhan_sh'],
        'lanzhou_sh': df_SH['lanzhou_sh'],
        'shenyang_sh': df_SH['shenyang_sh'],
        'yinni_sh': df_SH['yinni_sh']
    }

    palette = ["#c9d9d3", "#718dbf", "#e84d60", "#18A05E"]
    x = [(week, place) for week in week_num for place in pro_place]
    counts = sum(zip(data['wuhan_sh'], data['lanzhou_sh'], data['shenyang_sh'], data['yinni_sh']), ())  # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts, place=place))

    p = figure(x_range=FactorRange(*x), plot_width=2000, title="2018年四地生产商光缆护套（SH）oee指标分组柱状图(W:武汉、L：兰州、S：沈阳、Y：印尼)",
               plot_height=400,
               toolbar_location=None, tools=TOOLS)
    p.hover.tooltips = [('周数\生产商', "@x"), ('指标', "@counts")]
    p.vbar(x='x', top='counts', width=1, source=source, line_color="white", legend="place",
           fill_color=factor_cmap('x', palette=palette, factors=pro_place, start=1, end=2))

    p.y_range.start = 0
    p.x_range.range_padding = 0.01
    # p.xaxis.major_label_orientation = 0.5
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    show(p)


def figure_vbar_stack():
    f = open('../overview_oee/四地光缆OEE记录.csv', encoding='utf-8')
    df = pd.read_csv(f)
    df = df.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
    df1 = df.drop(df.index[16:])
    df1.set_index('Unnamed: 2', inplace=True)
    TOOLS = "pan,wheel_zoom,box_zoom,reset,tap,hover,save"
    colors = ["#c9d9d3", "#718dbf", "#e84d60", "#18A05E"]
    display = list(df1.index[3::4])
    data = {
        'x_label': list(df1.columns),
        display[0]: df1.loc[display[0]],
        display[1]: df1.loc[display[1]],
        display[2]: df1.loc[display[2]],
        display[3]: df1.loc[display[3]],
    }

    p = figure(x_range=list(df1.columns), plot_height=400, plot_width=1200, title="2018年四地生产商光缆护套（SH）oee指标堆叠柱状图",
               tooltips="$name @x_label: @$name", tools=TOOLS)
    p.vbar_stack(display, x='x_label', width=0.9, color=colors, source=data, legend=[x for x in ['W', 'L', 'S', 'Y']])

    p.y_range.start = 0
    p.x_range.range_padding = 0.05
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = 'top_left'
    p.legend.orientation = 'horizontal'
    p.legend.label_text_font_size = '10pt'
    p.legend.background_fill_alpha = 0
    p.legend.border_line_alpha = 0
    p.xaxis.major_label_orientation = 0.75

    show(p)
