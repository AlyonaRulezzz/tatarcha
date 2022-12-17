import sqlite3
from django.http import HttpResponse
from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot

# def home(request):
#     return HttpResponse('ola!)')


def home(request):
    def scatter():
        dbase = sqlite3.connect("baza.db")
        c = dbase.cursor()
        c.execute(
            "select exp, dates from data_xp where student_id = 245;"
        )
        res = c.fetchall()
        y1, x1 = zip(*res)
        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1) + 1000])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {
        'plot1': scatter()
    }

    return render(request, 'home.html', context)

