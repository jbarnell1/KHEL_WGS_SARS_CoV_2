from ..workflow_obj import workflow_obj
import pandas as pd
import datetime
import pandas_bokeh
import bokeh
import os


class plotter_obj(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "plotter"


    # methods
    def get_json(self):
        super().get_json(-6)


    def get_plotter_dfs(self):
        super().setup_db()
        self.df = self.db_handler.ss_read(query=self.read_query_tbl1)


    def create_plots(self):
        colors = []
        # Plot1 - Line plot
        p_line= self.df.groupby(['month']).mean().plot_bokeh(kind="line",y="sensor_2",color='#d01c8b',plot_data_points=True,show_figure=False)
        # Plot2- Barplot
        p_bar = self.df.groupby(['month']).mean().plot_bokeh(kind="bar",colormap=colors,show_figure=False)
        # Plot3- stacked bar chart
        df_sensor=df_random.drop(['month'],axis=1)
        p_stack=df_sensor.groupby(['category']).mean().plot_bokeh(kind='barh', stacked=True,colormap=colors,show_figure=False)
        #Plot4- Scatterplot
        p_scatter = df_random.plot_bokeh(kind="scatter", x="month", y="sensor_2",category="category",colormap=colors,show_figure=False)
        #Plot5- Pie chart
        p_pie= df_random.groupby(['category']).mean().plot_bokeh.pie(y='sensor_1',colormap=bokeh.palettes.Viridis256,show_figure=False)
        #Plot6- Histogram
        p_hist=df_sensor.plot_bokeh(kind='hist', histogram_type="stacked",bins=6,colormap=bokeh.palettes.Viridis256, show_figure=False)
        #Make Dashboard with Grid Layout: 
        pandas_bokeh.plot_grid([[p_line, p_bar,p_stack],[p_scatter, p_pie,p_hist]], plot_width=400)


    def write_data(self):
        today = datetime.datetime.today().strftime("mmddyy")
        num = 1
        file_name = today + "/interactive_plot_" + num + ".html"
        while os.path.exists(file_name):
            num += 1
            file_name = today + "/interactive_plot_" + num + ".html"
        file_path = self.base_path + file_name
        pandas_bokeh.output_file(file_path)