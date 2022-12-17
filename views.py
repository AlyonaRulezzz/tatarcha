import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from django_plotly_dash import DjangoDash
import django


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

django.conf.settings.configure({'DJANGO_SETTINGS_MODULE': 'PLOTLY_DASH'})
app = DjangoDash('XpPlot')

@app.callback(
    dash.dependencies.Output("time-series-chart", "figure"),
    dash.dependencies.Input("ticker", "value"))
def display_time_series(ticker):
    fig = px.line(df_xp.reset_index(), x='index', y=ticker)
    return fig

# {%load plotly_dash%}

# {%plotly_app name="XpPlot"%}
