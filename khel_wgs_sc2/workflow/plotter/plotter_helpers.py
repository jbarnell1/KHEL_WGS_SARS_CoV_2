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
        # # Plot1 - Line plot
        # p_line= self.df.groupby(['wgs_run_date']).mean().plot_bokeh(kind="line",y="sensor_2",color='#d01c8b',plot_data_points=True,show_figure=False)
        # # Plot2- Barplot
        # p_bar = self.df.groupby(['wgs_run_date']).mean().plot_bokeh(kind="bar",colormap=bokeh.palettes.Viridis256,show_figure=False)
        # # Plot3- stacked bar chart
        # df_sensor=self.df.drop(['wgs_run_date'],axis=1)
        # p_stack=df_sensor.groupby(['category']).mean().plot_bokeh(kind='barh', stacked=True,colormap=bokeh.palettes.Viridis256,show_figure=False)
        # #Plot4- Scatterplot
        # p_scatter = self.df.plot_bokeh(kind="scatter", x="wgs_run_date", y="sensor_2",category="category",colormap=bokeh.palettes.Viridis256,show_figure=False)
        # #Plot5- Pie chart
        # p_pie= self.df.groupby(['category']).mean().plot_bokeh.pie(y='sensor_1',colormap=bokeh.palettes.Viridis256,show_figure=False)
        # #Plot6- Histogram
        # p_hist=df_sensor.plot_bokeh(kind='hist', histogram_type="stacked",bins=6,colormap=bokeh.palettes.Viridis256, show_figure=False)
        today = datetime.datetime.today().strftime("mmddyy")
        num = 1
        file_name = today + "/interactive_plot_" + str(num) + ".html"
        while os.path.exists(file_name):
            num += 1
            file_name = today + "/interactive_plot_" + str(num) + ".html"
        file_path = self.base_path + file_name
        pandas_bokeh.output_file(file_path)

        #area_plot_df = self.df[["doc", "clade"]].copy()
        area_plot_df = self.df
        area_plot_df['date'] = self.df.apply(lambda row: row[:7], axis=1)
        area_plot_df = area_plot_df.groupby(['date', 'clade']).clade.agg(['count'])
        area_plot_df.reset_index(inplace=True)
        print(area_plot_df)
        area_plot_df = area_plot_df.pivot(index='date', columns='clade', values='count')
        area_plot_df.reset_index(inplace=True)
        area_plot_df = area_plot_df[["date", "21A", "21A (Delta)"]].copy()
        print(area_plot_df)
        self.area_plot = area_plot_df.plot_bokeh.area(
            x="date",
            stacked=True,
            normed=100,
            legend="top_left",
            colormap="Viridis",
            title="Clades of SARS-CoV-2 Over Time",
            xlabel="Date of Collection",
            ylabel="Percent of total")

        #Make Dashboard with Grid Layout: 
        #pandas_bokeh.plot_grid([[p_line, p_bar,p_stack],[p_scatter, p_pie,p_hist]], plot_width=400)


    def write_data(self):
        today = datetime.datetime.today().strftime("mmddyy")
        num = 1
        file_name = today + "/interactive_plot_" + num + ".html"
        while os.path.exists(file_name):
            num += 1
            file_name = today + "/interactive_plot_" + num + ".html"
        file_path = self.base_path + file_name
        pandas_bokeh.output_file(file_path)