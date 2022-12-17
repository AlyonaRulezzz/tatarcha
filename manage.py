#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from django_plotly_dash import DjangoDash
import django

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttx.settings')

    excel_path = '/Users/milkfist/Downloads/PROGRESS_DATA.xlsx'

    progress_data_xp = pd.read_excel(excel_path, sheet_name='Данные по хр')
    progress_data_xp = progress_data_xp.rename(columns={'Номер участника': 'pid'})
    progress_data_xp = progress_data_xp.set_index('pid')
    current_dates_xp = pd.Series(progress_data_xp.columns)
    full_dates_xp = pd.Series(pd.date_range(min(current_dates_xp), max(current_dates_xp)))
    missing_dates_xp = pd.Series(list(set(full_dates_xp) - set(current_dates_xp))).sort_values()
    tmp = pd.DataFrame(index=progress_data_xp.index, columns=missing_dates_xp)
    df_xp = pd.concat([progress_data_xp, tmp], axis=1).sort_index(axis=1)
    df_xp = df_xp.apply(pd.to_numeric).interpolate('linear', axis=1)
    df_xp = df_xp.transpose().reset_index()

    app = DjangoDash('XpPlot')

    app.layout = html.Div([
        html.H4('XP mining'),
        dcc.Graph(id="time-series-chart"),
        html.P("Select student id:"),
        dcc.Dropdown(
            id="ticker",
            options=list(df_xp.columns[1:]),
            value=df_xp.columns[1],
            clearable=False,
        ),
    ])

    @app.callback(
        dash.dependencies.Output("time-series-chart", "figure"),
        dash.dependencies.Input("ticker", "value"))
    def display_time_series(ticker):
        fig = px.line(df_xp.reset_index(), x='index', y=ticker)
        return fig

    # {%load plotly_dash%}
    # {%plotly_app name="XpPlot"%}

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
