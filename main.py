import dash_table
from dash import Dash, html, dcc, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dash_table import DataTable
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from smo import SMO

theme = dbc.themes.JOURNAL
# App Instance

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(value='tab1', label='Пошаговый режим', children=[
            html.H4(children='Результат работы СМО в пошаговом режиме')]),
        dcc.Tab(value='tab2', label='Автоматическмй режим', children=[
            html.H4(children='Результат работы СМО в автоматическом режиме')
        ])
    ]),
    html.Div(id='begin', children=[html.H6(children="Введите количество источников"),
                                   dcc.Input(id='source', type='number', value='2', style={'width': '16.65%'}),
                                   html.H6(children="Введите количество заявок"),
                                   dcc.Input(id='request', type='number', value='5', style={'width': '16.65%'}),
                                   html.H6(children="Введите количество буфферов"),
                                   dcc.Input(id='buff', type='number', value='2', style={'width': '16.65%'}),
                                   html.H6(children="Введите количество приборов"),
                                   dcc.Input(id='device', type='number', value='2', style={'width': '16.65%'}),
                                   html.Div(id='begin_but'),
                                   html.Div(id='begin_but2')]),
    html.Div(id='table1', children=[html.Div(id='after', children=html.Button('Следующий шаг'))])

])

smo = SMO(2, 5, 2, 2)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame(
#     smo.current_state
# )

@app.callback(
    [Output(component_id='table1', component_property='children'),
     Output(component_id='begin_but', component_property='children'),
     Output(component_id='begin_but2', component_property='children'),
     Output("begin_but", "n_clicks"),
     Output("begin_but2", "n_clicks"),
     Output("after", "n_clicks")],
    [Input(component_id='tabs', component_property='value'),
     Input(component_id='begin_but', component_property='n_clicks'),
     Input(component_id='begin_but2', component_property='n_clicks'),
     Input(component_id='after', component_property='n_clicks')],
    [State(component_id='source', component_property='value'),
     State(component_id='request', component_property='value'),
     State(component_id='buff', component_property='value'),
     State(component_id='device', component_property='value')],
    prevent_initial_call=False
)
def update_output(tab, n_clicks_begin, n_clicks_begin_2, n_clicks_after, source_amount, request_amount, buff_amount,
                  device_amount):
    if tab == 'tab1':
        if n_clicks_begin is None:
            return [html.H5(children='Календарь событий'),
                    DataTable(editable=True),
                    html.H5(children='Буфферы'),
                    DataTable(editable=True),
                    html.Div(id='after', children=html.Button('Следующий шаг'))], [
                       html.Button('Сгенерировать СМО')], None, 0, None, 0
        else:
            if n_clicks_begin == 1:
                print(n_clicks_begin)
                global smo
                smo = SMO(int(source_amount), int(request_amount), int(buff_amount), int(device_amount))
                return [html.H5(children='Календарь событий'),
                        DataTable(data=pd.DataFrame(smo.current_state).to_dict('records'), editable=True),
                        html.H5(children='Буфферы'),
                        DataTable(pd.DataFrame(smo.current_state_buf).to_dict('records'), editable=True),
                        html.P("Время рабты СМО: " + str(smo.total_time)),
                        html.Div(id='after', children=html.Button('Следующий шаг'))], [
                           html.Button('Сгенерировать СМО')], None, 0, None, 0
            if n_clicks_after:
                if smo.queue_source or smo.queue_device:
                    print(smo.current_state)
                    smo.iteration()
                    return [html.H5(children='Календарь событий'),
                            DataTable(data=pd.DataFrame(smo.current_state).to_dict('records'), editable=True),
                            html.H5(children='Буфферы'),
                            DataTable(pd.DataFrame(smo.current_state_buf).to_dict('records'), editable=True),
                            html.P("Время рабты СМО: " + str(smo.total_time)),
                            html.Div(id='after', children=html.Button('Следующий шаг'))], [
                               html.Button('Сгенерировать СМО')], None, 0, None, n_clicks_after
                else:
                    return [html.H5(children='Календарь событий'),
                            DataTable(data=pd.DataFrame(smo.current_state).to_dict('records'), editable=True),
                            html.H5(children='Буфферы'),
                            DataTable(data=pd.DataFrame(smo.current_state_buf).to_dict('records'), editable=True),
                            html.P("Время рабты СМО: " + str(smo.total_time)),
                            html.Div(id='after')], [
                               html.Button('Сгенерировать СМО')], None, 0, None, None
    elif tab == 'tab2':
        if n_clicks_begin_2 is None:
            return [html.H5(children='Источники'),
                    DataTable(editable=True),
                    html.H5(children='Приборы'),
                    DataTable(editable=True),
                    html.Div(id='after')], None, [
                       html.Button('Сгенерировать СМО')], n_clicks_begin, 0, n_clicks_after
        else:
            if n_clicks_begin_2 == 1:
                smo = SMO(int(source_amount), int(request_amount), int(buff_amount), int(device_amount))
                smo.all_iteration()
                print("я здесь был")
                return [html.H5(children='Источники'),
                        DataTable(data=pd.DataFrame(smo.source_charact).to_dict('records'), editable=True),
                        html.H5(children='Приборы'),
                        DataTable(data=pd.DataFrame(smo.device_charact).to_dict('records'), editable=True),
                        html.Div(id='after')
                        ], None, [
                           html.Button('Сгенерировать СМО')], None, 0, None


if __name__ == '__main__':
    app.run_server(debug=True)
