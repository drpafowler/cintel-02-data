import seaborn as sns

# Import data from shared.py
from shared import app_dir, df
import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  


ui.page_opts(title=ui.h1("Philip's Penguins", style="text-align: center;"), fillable=True)


with ui.sidebar(title=ui.h2("Global Controls"), width="400px"):
    ui.input_select("xaxis", "X-axis (all plots)", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_length_mm")
    ui.input_select("plot", "Plot Type", ["Scatterplot", "Histogram"])
    ui.input_select("yaxis", "Scatterplot Y-axis", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_depth_mm")
    ui.input_select("hue_control", "Hue Control", ["sex", "species", "island"], selected="species")
    ui.h4("Filter Controls")
    ui.input_switch("filter", "Filter Data", True)
    ui.input_slider("mass", "Mass", 2000, 6000, [2000,6000])
    ui.input_checkbox_group(
        "sex",
        "Sex",
        ["Male", "Female"],
        selected=["Male", "Female"],
    )
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.input_checkbox_group(
        "island",
        "Island",
        ["Biscoe", "Dream", "Torgersen"],
        selected=["Biscoe", "Dream", "Torgersen"],
    )   
    ui.hr()
    ui.h4("Seaborn Controls")

    ui.input_slider("bins", "Number of bins", 5, 50, 20)

    ui.hr()
    ui.h4("Plotly Controls")
    ui.input_numeric("plotly_bins", "Number of bins", 20, min=5, max=50)

    ui.a("GitHub", href="https://github.com/drpafowler/cintel-02-data", target="_blank")



with ui.layout_column_wrap(fill=False):
    with ui.value_box():
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box():
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box():
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"
    
    with ui.value_box():
        "Average body mass"

        @render.text
        def body_mass():
            return f"{filtered_df()['body_mass_g'].mean():.1f} g"

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Seaborn Penguin Data Visualisation")

        @render.plot
        def length_depth():
            if input.plot() == "Scatterplot":
                if input.filter():
                    return sns.scatterplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                        hue=input.hue_control(),
                    )
                else:
                    return sns.scatterplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        y=input.yaxis(),
                    )
            elif input.plot() == "Histogram":
                if input.filter():
                    return sns.histplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        bins=input.bins(),
                        hue=input.hue_control(),
                        multiple="stack",
                    )
                else:
                    return sns.histplot(
                        data=filtered_df(),
                        x=input.xaxis(),
                        bins=input.bins(),
                    )

    with ui.card(full_screen=True):
        ui.card_header("Plotly Penguin Data Visualisation")

        @render_widget
        def plotly_plot():
            if input.plot() == "Scatterplot":
                if input.filter():
                    fig = px.scatter(
                    filtered_df(),
                    x=input.xaxis(),
                    y=input.yaxis(),
                    color=input.hue_control(),
                    title="Scatterplot of Penguin Data"
                    )
                else:
                    fig = px.scatter(
                    filtered_df(),
                    x=input.xaxis(),
                    y=input.yaxis(),
                    title="Scatterplot of Penguin Data"
                    )
            elif input.plot() == "Histogram":
                if input.filter():
                    fig = px.histogram(
                    filtered_df(),
                    x=input.xaxis(),
                    color=input.hue_control(),
                    marginal="box",
                    title="Histogram of Penguin Data",
                    nbins=input.plotly_bins()
                    )
                else:
                    fig = px.histogram(
                    filtered_df(),
                    x=input.xaxis(),
                    marginal="box",
                    title="Histogram of Penguin Data",
                    nbins=input.plotly_bins()
                    )
            return fig


with ui.layout_columns():

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")
        ui.input_switch("show_table", "Switch on to show a data table", False)
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
                "sex",
            ]
            if input.show_table():
                return render.DataTable(filtered_df()[cols], filters=True)
            else:
                return render.DataGrid(filtered_df()[cols], filters=True)
    with ui.card(full_screen=True):
        ui.card_header("Penguin Correlation Table")
        @render.plot
        def correlation_heatmap():
            cols = ["bill_length_mm", "bill_depth_mm", "body_mass_g"]
            corr = filtered_df()[cols].corr()
            return sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    if not input.filter():
        return df
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df[filt_df["sex"].isin(input.sex())]
    filt_df = filt_df[filt_df["island"].isin(input.island())]
    filt_df = filt_df.loc[(filt_df["body_mass_g"] >= input.mass()[0]) & (filt_df["body_mass_g"] <= input.mass()[1])]
    return filt_df
