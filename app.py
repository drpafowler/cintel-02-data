import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df
import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget  


ui.page_opts(title=ui.h1("Philip's Penguins", style="text-align: center;"), fillable=True)


with ui.sidebar(title=ui.h2("Seaborn Controls")):
    ui.input_select("plot", "Plot Type", ["Scatterplot", "Histogram"])
    ui.input_select("xaxis", "X-axis", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_length_mm")
    ui.input_select("yaxis", "Scatterplot Y-axis", ["bill_length_mm", "bill_depth_mm", "body_mass_g"], selected="bill_depth_mm")
    ui.input_slider("bins", "Number of bins", 5, 50, 20)
    ui.input_slider("mass", "Mass", 2000, 6000, [2000,6000])

    ui.h3("Plotly Controls")
    ui.input_numeric("plotly_bins", "Number of bins", 20, min=5, max=50)

    ui.h3("Filters")
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
                return sns.scatterplot(
                    data=filtered_df(),
                    x=input.xaxis(),
                    y=input.yaxis(),
                    hue="species",
                )
            elif input.plot() == "Histogram":
                return sns.histplot(
                    data=filtered_df(),
                    x=input.xaxis(),
                    bins=input.bins(),
                    hue="species",
                    multiple="stack",
                )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

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
            return render.DataGrid(filtered_df()[cols], filters=True)

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram")

        @render_widget
        def plotly_plot():
            fig = px.histogram(
            filtered_df(),
            x=input.xaxis(),
            color="species",
            marginal="box",
            title="Histogram of Penguin Data",
            nbins=input.plotly_bins()
            )
            return fig

        

ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df[filt_df["sex"].isin(input.sex())]
    filt_df = filt_df[filt_df["island"].isin(input.island())]
    filt_df = filt_df.loc[(filt_df["body_mass_g"] >= input.mass()[0]) & (filt_df["body_mass_g"] <= input.mass()[1])]
    return filt_df
