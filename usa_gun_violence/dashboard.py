import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from usa_gun_violence.datareader import DataReader, usa_states

gun_violence_data_reader = DataReader()
nb_injured_and_killed_by_year = gun_violence_data_reader.get_nb_injured_and_killed_by_year()
nb_injured_and_killed_by_state = gun_violence_data_reader.get_nb_injured_and_killed_by_state()

colorscale = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
       [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

nb_injured_and_killed_by_state['hover_text'] = nb_injured_and_killed_by_state.index.map(lambda x: usa_states.get(x)) + '<br>' + \
             'Number of people killed : ' + nb_injured_and_killed_by_state['n_killed'].astype(str) + '<br>' + \
             'Number of people injured : ' + nb_injured_and_killed_by_state['n_injured'].astype(str) + '<br>'

data = [dict(
    type='choropleth',
    colorscale=colorscale,
    autocolorscale=False,
    locations=nb_injured_and_killed_by_state.index,
    z=nb_injured_and_killed_by_state['total_injured_killed'].astype(int),
    locationmode='USA-states',
    text=nb_injured_and_killed_by_state['hover_text'],
    marker=dict(
        line=dict(
            color='rgb(255,255,255)',
            width=2
        )),
    colorbar=dict(
        title="Millions USD")
)]

layout = dict(
    title='Number of victims by states between 2013 and 2017',
    height=500,
    width=900,
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'),
)

fig = dict(data=data, layout=layout)

layout = html.Div([
    html.H1('United States Gun Violence Study'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Graph(
        id='county-choropleth',
        figure=fig
    ),
    dcc.Graph(
        id='example-graph',
        figure={
            'layout': {
                'title': 'Gun violence evolution between 2013 and 2017 in the USA',
                'height': 500,
                'width': 850
            },
            'data': [
                {
                    'x': nb_injured_and_killed_by_year.n_injured.index,
                    'y': nb_injured_and_killed_by_year.n_injured,
                    'type': 'bar',
                    'name': 'People injured'
                },
                {
                    'x': nb_injured_and_killed_by_year.n_killed.index,
                    'y': nb_injured_and_killed_by_year.n_killed,
                    'type': 'bar',
                    'name': 'People killed'
                },
            ]
        }
    )
])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)