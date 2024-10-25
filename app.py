from shiny.express import input, render, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins

ui.page_opts(title="Philip's Penguins", fillable=True)

with ui.sidebar():
    ui.input_selectize(
        "xvar", "Select x-axis variable",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year"]
    )
    ui.input_numeric("bins", "Number of histogram bins", 30)
    
    ui.input_selectize(
        "yvar", "Select scatterplot y-axis variable",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year"]
    )
    ui.input_selectize(
        "plot_type", "Select plot type",
        ["Histogram", "Scatterplot"]
    )
    ui.input_selectize(
        "color_by", "Color scatterplot by",
        ["off", "species", "sex", "island"]
    )

with ui.card(full_screen=True):
    @render_plotly
    def plot():
        import plotly.express as px
        penguins = load_penguins()
        plot_type = input.plot_type()
        
        if plot_type == "Histogram":
            return px.histogram(penguins, x=input.xvar(), nbins=input.bins())
        elif plot_type == "Scatterplot":
            color_by = input.color_by()
            if color_by == "off":
                return px.scatter(penguins, x=input.xvar(), y=input.yvar())
            else:
                return px.scatter(penguins, x=input.xvar(), y=input.yvar(), color=color_by)