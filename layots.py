# import dash_table
# import pandas as pd
# from dash import html, Output, Input
# import dash_bootstrap_components as dbc
# from dash import Dash, html, dcc
# import plotly.express as px
# from dash.exceptions import PreventUpdate
#
#
#
# def nav_bar():
#     """
#     Creates Navigation bar
#     """
#     navbar = html.Div(
#         [
#             html.H4("СМО", className="display-10", style={'textAlign': 'center'}),
#             # html.Hr(),
#             dbc.Nav(
#                 [
#                     dbc.NavLink("Пошаговый режим", href="/page1", active="exact", external_link=True),
#                 ],
#                 pills=True,
#                 vertical=True
#             ),
#         ]
#     )
#     return navbar
#
#
# # # graph 1
# # example_graph1 = px.scatter(df, x="sepal_length", y="sepal_width", color="species")
# #
# # # graph 2
# # example_graph2 = px.histogram(df, x="sepal_length", color="species", nbins=20)
# # example_graph2.update_layout(barmode='overlay')
# # example_graph2.update_traces(opacity=0.55)
#
# #####################################
# # Create Page Layouts Here
# #####################################
#
# ### Layout 1
# layout1 = html.Div([
#     html.H4(children='Результат работы СМО в пошаговом режиме'),
#     dash_table.DataTable(id='table'),
#     html.Button('Следующий шаг', id='show-secret')
# ])
#
