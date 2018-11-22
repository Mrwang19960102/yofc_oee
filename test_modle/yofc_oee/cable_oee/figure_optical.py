import pandas as pd
import numpy as np
from bokeh.io import show, output_notebook
output_notebook()
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from datetime import datetime
from bokeh.models import NumeralTickFormatter,LabelSet

df = pd.read_excel('./overview_optical/OEE报表开发需求（武汉光纤）.xlsx',sheet_name='OEE-Chart',header=4,encoding = "utf-8")[1:13]
df = df.replace(np.NaN,0)
time_list = []
for i in df['日期\nDATE'].dt.strftime('%Y-%m-%d'):
    time_list.append(i[0:7])

def get_data(column):
    data = {
        column.lower(): df[column],
        'time': time_list,
        'per_'+column.lower(): df[column].apply(lambda x: format(x, '.2%'))
    }
    return data
def figure_line(column):
    """
    绘制折线图
    :return:
    """
    data = get_data(column)
    source = ColumnDataSource(data=data)
    p = figure(x_range=time_list, plot_width=820, plot_height=300, title=column,
               toolbar_location=None,y_range=[0,df[column].max()*1.1],x_axis_label='时间/月份',y_axis_label='百分比')
    p.line('time', column.lower(), source=source, line_width=3)
    p.square('time', column.lower(), size=5, color="red", source=source)
    labels = LabelSet(x='time', y = column.lower(), text='per_'+column.lower(), x_offset=-17, y_offset=5, source=source,
                      render_mode='canvas', text_font_size="8pt")
    p.add_layout(labels)
    p.xgrid.grid_line_color = None
    p.y_range.start = -0.02
    p.yaxis[0].formatter = NumeralTickFormatter(format="0.00%")
    show(p)

def figure_vbar(column):
    """
    绘制柱状图
    :param column:
    :return:
    """
    data = get_data(column)
    source = ColumnDataSource(data=data)
    p = figure(x_range=time_list, plot_width=820, plot_height=300, title=column,y_range=[0,df[column].max()*1.15],
               toolbar_location=None, x_axis_label='时间/月份',y_axis_label='百分比')
    p.vbar(x='time', top=column.lower(), width=0.4, source=source)
    labels = LabelSet(x='time', y=column.lower(), text='per_'+column.lower(), x_offset=-13, y_offset=5,source=source,text_font_size = "8pt")
    p.add_layout(labels)

    p.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    show(p)
