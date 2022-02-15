# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python [conda env:532]
#     language: python
#     name: conda-env-532-py
# ---

import altair as alt
import pandas as pd
from dash import Dash, dcc, html, Input, Output

alt.data_transformers.disable_max_rows()

# Read in global data
gm = pd.read_csv("https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv",
                 parse_dates = ['year'])

gm2000 = gm.query("year == 2000")

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='children_per_woman', 
        options=[{'label': col, 'value': col} for col in gm2000.columns])])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'), 
    Input('xcol-widget', 'value'))

def plot_altair(xcol):
    chart = alt.Chart(gm2000).mark_circle().encode(
        x = xcol,
        y = 'life_expectancy',
        tooltip='children_per_woman').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)