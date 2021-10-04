from bokeh.models.tools import HoverTool
from ..workflow_obj import workflow_obj
import re
import pandas as pd
from bokeh.palettes import Spectral11, viridis, d3, Turbo256
from bokeh.plotting import figure, save, show, output_file, ColumnDataSource
import datetime


class plotter_obj(workflow_obj):
    # constructor
    def __init__(self):
        self.id = "plotter"

    
    # methode
    def get_json(self):
        super().get_json(-6)

    def get_plots(self):
        super().setup_db()
        everything = self.db_handler.sub_read(query=self.read_query_tbl1)
        everything.to_csv(self.base_path + "test.csv")
        print("\nBuilding clade over time plot...")
        self.plot_clades_over_time(everything)
        print(" Done!")
        print("\nBuilding aa_subs over time plot...")
        self.plot_important_aa_subs_over_time(everything)
        print(" Done!")
        print("\nBuilding cumulative subs over time plot...")
        self.plot_cumulative_subs_over_time(everything)
        print(" Done!")
        print("\nBuilding Deltas over time plot...")
        self.plot_delta_over_time(everything)
        print(" Done!")
        print("\nBuilding lineages over time plot...")
        self.plot_lineage_over_time(everything)
        print(" Done!")
        


    def plot_clades_over_time(self, everything):
        cot = everything[['doc', 'clade', 'hsn']].copy()
        cot = cot.groupby(['doc', 'clade']).agg(['count'])
        cot.reset_index(inplace=True)
        cot_pvt = cot.pivot(index='doc', columns='clade')
        cot_pvt.fillna(value=0, inplace=True)
        cot_pvt.columns = [col[2] for col in cot_pvt.columns]
        for combine_lst_key in self.cot_combine_cols.keys():
            for col_name_idx in range(len(self.cot_combine_cols[combine_lst_key])):
                if col_name_idx == 0:
                    temp_col = cot_pvt[self.cot_combine_cols[combine_lst_key][col_name_idx]]
                else:
                    temp_col += cot_pvt[self.cot_combine_cols[combine_lst_key][col_name_idx]]
            cot_pvt[combine_lst_key] = temp_col
            cot_pvt.drop(labels=self.cot_combine_cols[combine_lst_key], inplace=True, axis=1)
        cot_pvt.reset_index(inplace=True)
        cot_pvt['date'] = cot_pvt.apply(lambda row: get_dt(row), axis=1)
        clades = cot_pvt.columns.tolist()
        clades.remove('date')
        clades.remove('doc')
        cot_pvt = cot_pvt.resample('W', on='date').sum()
        cot_pvt.reset_index(inplace=True)
        cot_pvt['total'] = cot_pvt.apply(lambda row: get_total(row, clades), axis=1)
        for clade in clades:
            cot_pvt[clade + "f"] = cot_pvt.apply(lambda row: get_percentage(row, clade), axis=1)
        cot_pvt.drop(labels=clades, inplace=True, axis=1)
        cot_pvt.drop(labels=['total'], inplace=True, axis=1)
        cot_pvt.columns = [column[:-1] for column in cot_pvt.columns]
        
        source = ColumnDataSource(cot_pvt)
        output_file(self.base_path + "cot_pvt.html")
        # create a new plot with a title and axis labels
        p = figure(
            title="Clades over time",
            x_axis_label='Time',
            x_axis_type='datetime',
            y_range=(0, 1),
            y_axis_label='Percent dominance',
            sizing_mode='stretch_both'
        )
        stackers = cot_pvt.columns.tolist()
        #stackers.remove('do')
        stackers.remove('dat')
        #add a line renderer with legend and line thickness to the plot
        p.varea_stack(
            stackers=stackers,
            x='dat',
            color=viridis(len(stackers)),
            legend_label=stackers,
            source=source
        )
        p.vline_stack(
            stackers=stackers,
            x='dat',
            color=viridis(len(stackers)),
            source=source
        )
        p.legend.orientation='horizontal'
        p.legend.location='top_center'
        p.legend.background_fill_color = '#fafafa'
        # show the results
        save(p)    

    def plot_lineage_over_time(self, everything):
        lot = everything[['doc', 'lineage_id', 'hsn']].copy()
        lot = lot.groupby(['doc', 'lineage_id']).agg(['count'])
        lot.reset_index(inplace=True)
        lot_pvt = lot.pivot(index='doc', columns='lineage_id')
        lot_pvt.fillna(value=0, inplace=True)
        lot_pvt.columns = [col[2] for col in lot_pvt.columns]
        for combine_lst_key in self.lot_combine_cols.keys():
            for col_name_idx in range(len(self.lot_combine_cols[combine_lst_key])):
                if col_name_idx == 0:
                    temp_col = lot_pvt[self.lot_combine_cols[combine_lst_key][col_name_idx]]
                else:
                    temp_col += lot_pvt[self.lot_combine_cols[combine_lst_key][col_name_idx]]
            lot_pvt[combine_lst_key] = temp_col
            lot_pvt.drop(labels=self.lot_combine_cols[combine_lst_key], inplace=True, axis=1)
        lot_pvt.reset_index(inplace=True)
        lot_pvt['date'] = lot_pvt.apply(lambda row: get_dt(row), axis=1)
        lineages = lot_pvt.columns.tolist()
        lineages.remove('date')
        lineages.remove('doc')
        lot_pvt = lot_pvt.resample('W', on='date').sum()
        lot_pvt.reset_index(inplace=True)
        lot_pvt['total'] = lot_pvt.apply(lambda row: get_total(row, lineages), axis=1)
        for lineage in lineages:
            lot_pvt[lineage + "f"] = lot_pvt.apply(lambda row: get_percentage(row, lineage), axis=1)
        lot_pvt.drop(labels=lineages, inplace=True, axis=1)
        lot_pvt.drop(labels=['total'], inplace=True, axis=1)
        lot_pvt.columns = [column[:-1] for column in lot_pvt.columns]
        
        source = ColumnDataSource(lot_pvt)
        output_file(self.base_path + "lot_pvt.html")
        pd.DataFrame(lot_pvt).to_csv(self.base_path + "lot_pvt.csv")
        # create a new plot with a title and axis labels
        p = figure(
            title="lineages over time",
            x_axis_label='Time',
            x_axis_type='datetime',
            y_range=(0, 1),
            y_axis_label='Percent dominance',
            sizing_mode='stretch_both'
        )
        stackers = lot_pvt.columns.tolist()
        #stackers.remove('do')
        stackers.remove('dat')
        #add a line renderer with legend and line thickness to the plot
        p.varea_stack(
            stackers=stackers,
            x='dat',
            color=viridis(len(stackers)),
            legend_label=stackers,
            source=source
        )
        p.vline_stack(
            stackers=stackers,
            x='dat',
            color=viridis(len(stackers)),
            source=source
        )
        p.legend.orientation='vertical'
        p.legend.location='top_left'
        p.legend.background_fill_color = '#fafafa'
        # show the results
        save(p)    

    def plot_important_aa_subs_over_time(self, everything):
        ast = everything[['doc', 'aa_substitutions']].copy()
        ast['doc'] = pd.to_datetime(ast['doc'], format="%Y-%m-%d")
        for col_to_add in self.ast_add_cols:
            self.n = 0
            ast[col_to_add] = ast.apply(lambda row: self.get_num_occurances(row, self.ast_add_cols[col_to_add]), axis=1)
        ast.drop(labels=['aa_substitutions'], inplace=True, axis=1)
        ast = ast.resample('D', on='doc').sum()
        for col in self.ast_add_cols.keys():
            ast[col] = ast[col].cumsum()
        

        p = figure(
            title="Mutations evading treatment per CDC",
            x_axis_label='Date',
            x_axis_type='datetime',
            y_axis_label='Cumulative number of strains',
            sizing_mode='stretch_both',
        )
        output_file(self.base_path + "ast.html")
        num_lines=len(ast.columns)
        cols = [ast[name].values for name in ast]
        colors_list=Spectral11[0:num_lines]
        legends_list=ast.columns.tolist()
        xs=[ast.index.values]*num_lines
        ys=cols

        for (colr, leg, x, y) in zip(colors_list, legends_list, xs, ys):
            p.line(x, y, color=colr, line_width=3, legend_label=leg, hover_color=colr)

        p.legend.location='top_left'
        p.legend.background_fill_color = '#fafafa'

        save(p)


    def plot_cumulative_subs_over_time(self, everything):
        cst = everything[['doc', 'aa_substitutions', 'total_mutations']].copy()
        print(cst)
        cst['doc'] = pd.to_datetime(cst['doc'], format="%Y-%m-%d")
        cst['avg_tot_aa'] = cst.apply(lambda row: get_len(row, 'aa_substitutions'), axis=1)
        print(cst)
        cst.fillna(0, inplace=True)
        cst.drop(labels=['aa_substitutions'], inplace=True, axis=1)
        cst = cst.resample('W', on='doc').mean()
        cst.fillna(0, inplace=True)
        cst['diff'] = cst.apply(lambda row: row['total_mutations'] - row['avg_tot_aa'], axis=1)
        print(cst)

        p = figure(
            title="Number of mutations/substitutions over time",
            x_axis_label='Date',
            x_axis_type='datetime',
            y_axis_label='Total number of mutations/substitutions',
            sizing_mode='stretch_both',
        )
        output_file(self.base_path + "cst.html")
        num_lines=len(cst.columns)
        cols = [cst[name].values for name in cst]
        colors_list=Spectral11[0:num_lines]
        legends_list=cst.columns.tolist()
        xs=[cst.index.values]*num_lines
        ys=cols

        for (colr, leg, x, y) in zip(colors_list, legends_list, xs, ys):
            p.line(x, y, color=colr, line_width=3, legend_label=leg, hover_color=colr)

        p.legend.location='top_left'
        p.legend.background_fill_color = '#fafafa'

        save(p)

    def plot_delta_over_time(self, everything):
        dot = everything[['doc', 'clade', 'lineage_id']].copy()
        dot.fillna("", inplace=True)
        dot = dot.loc[dot['clade'].str.contains('21A')]
        dot['doc'] = pd.to_datetime(dot['doc'], format="%Y-%m-%d")
        dot.drop(labels=['clade'], inplace=True, axis=1)
        cols_to_create = set(dot.lineage_id.values.astype(str).tolist())
        cols_to_create.remove('B.1.617.2\xa0')
        for col in cols_to_create:
            dot[col] = dot.apply(lambda row: sum_types(row, col), axis=1)

        print(dot)
        dot = dot.resample('D', on='doc').sum()
        print(dot)
        for col in cols_to_create:
            dot[col] = dot[col].cumsum()
        print(dot)

        p = figure(
            title="Delta lineages over time",
            x_axis_label='Date',
            x_axis_type='datetime',
            y_axis_label='Cumulative number of lineages',
            sizing_mode='stretch_both',
        )
        output_file(self.base_path + "dot.html")
        num_lines=len(dot.columns)
        cols = [dot[name].values for name in dot]
        interval = 256/num_lines
        colors_list=[]
        for i in range(0, 256, int(interval)):
            colors_list.append(Turbo256[i])
        legends_list=dot.columns.tolist()
        xs=[dot.index.values]*num_lines
        ys=cols

        for (colr, leg, x, y) in zip(colors_list, legends_list, xs, ys):
            p.line(x, y, color=colr, line_width=5, legend_label=leg, hover_color=colr)

        p.legend.location='top_left'
        p.legend.background_fill_color = '#fafafa'

        dot.to_csv(self.base_path + "dot.csv")
        save(p)


    
    def get_num_occurances(self, row, lst):
        if pd.isna(row['aa_substitutions']):
            return 0
        for mut in lst:
            if not re.search(mut, row['aa_substitutions']):
                return 0
        return 1

def sum_types(row, col):
    if row['lineage_id'] == col:
        return 1
    return 0

def get_dt(row):
    dt = datetime.datetime.strptime(row['doc'], "%Y-%m-%d")
    return dt


def get_total(row, lst):
    total = 0
    for col in lst:
        total+= row[col]
    return total


def get_percentage(row, col):
    try:
        return row[col]/row['total']
    except ZeroDivisionError:
        return 0


def get_len(row, col):
    if pd.isna(row[col]):
        return 0
    lst = row[col].split(",")
    return float(len(lst))


