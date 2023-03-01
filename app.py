# -*- coding: utf-8 -*-

# visit http://127.0.0.1:8050/ in your web browser.

# Load libraries
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import ast

# Styles - CERULEAN (!), COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA (!),
# MINTY, PULSE (!), SANDSTONE (!), SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB (!), SUPERHERO, UNITED (!), YETI (!)
external_stylesheets = [dbc.themes.PULSE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,  # , external_stylesheets=external_stylesheets
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )
server = app.server

# Load course list
file = open("assets/courselist.txt", "r", encoding='utf-8')
# courses_list = json.load(f)
contents = file.read()
dictionary = ast.literal_eval(contents)
file.close()


# Camera angle for the plot
camera = dict(
    eye=dict(x=2, y=2, z=0.8)
)


# Function for formatting each annotation
def annotation(x, y, z, text, anchor, color):
    return dict(
        showarrow=False,
        x=x,
        y=y,
        z=z,
        text=text,
        xanchor=anchor,
        xshift=-2,
        yshift=10,
        opacity=1,
        font=dict(
            color=color,
            size=14
        ),
    )


# Function for formatting each axis
def axis(backgroundcolor):
    return dict(
        nticks=6, range=[0,1],
        backgroundcolor=backgroundcolor,
        gridcolor="white",
        showbackground=True,
        zerolinecolor="white",
        showspikes=False)


# Create dataframe for visualising 'Complete learning acquisition landscape'
df_tele = pd.DataFrame(data=[['too complicated content', 0.222, 0.111, 0.666],
                             ['too easy content', 0, 1, 0, ],
                             ['ideally matching content', 0.667, 0.333, 0]],
                       columns=['content', 'N-P', 'P-P', 'X-N'], index=None)

# Initial figure with the learning landscape and without 3d scatter
fig = go.Figure(data=[
    go.Mesh3d(
        x=df_tele['N-P'],
        y=df_tele['P-P'],
        z=df_tele['X-N'],
        color='steelblue',
        opacity=0.3,
        hoverinfo='skip',
    )
])

fig.update_layout(
    template='plotly',
    scene_camera=camera,
    scene=dict(
        xaxis_title="N-P",
        yaxis_title="P-P",
        zaxis_title="X-N",
        xaxis=axis("rgb(200, 200, 230)"),
        yaxis=axis("rgb(230, 200,230)"),
        zaxis=axis("rgb(230, 230,200)"),
        annotations=[
            annotation(0.222, 0.111, 0.666, '<b>Nepiemērots</b>', 'center', 'indianred'),
            annotation(0.667, 0.333, 0, '<b>Piemērots</b>', 'right', 'mediumseagreen'),
            annotation(0, 1, 0, '<b>Viegls</b>', 'left', 'royalblue')
        ],
    ),
    height=600,
    margin=dict(
        r=0, l=0,
        b=0, t=0),
)


# load dataframe from API
def loader(x):
    api = x
    df2 = pd.read_json(api, orient="split")

    df1 = pd.DataFrame(df2['user'].values.tolist())
    df1.columns = 'user_' + df1.columns
    col = df2.columns.difference(['user'])
    df2 = pd.concat([df2[col], df1], axis=1)
    return df2


# Clean and sort dataframe
def cleaner(x):
    # Select only rows with results value for type
    rez = x[x["type"] == "result"]

    # Filter out only first item in 'user_role'
    rez = rez.loc[np.array(list(map(len, rez.user_roles.values))) == 1]

    # Convert column from list to string
    rez['user_roles'] = rez['user_roles'].apply(lambda z: ','.join(map(str, z)))

    # Select only 'student' roles and make copy of original dataframe to avoid slicing view
    rez = rez.loc[rez.user_roles == 'student'].copy()

    # Transform time feature to datetime object
    rez["datetime"] = pd.to_datetime(rez["datetime"])

    # Keeping only first occurrence and dropping all other
    rez = rez.drop_duplicates(subset=['user_id', 'itemid'], keep="first")

    # Drop unnecessary columns
    rez.drop(['id', 'answer', 'answer_submitted', 'question', 'timestamp', 'type', 'user_roles'], axis=1,
             inplace=True)

    # Convert everything to uppercase in case there are some in lowercase
    rez['title'] = rez['title'].str.upper()

    # Take last
    rez['letter'] = rez['title'].str.strip().str[-1]

    # Remove rows that are not a or b
    rez = rez[(rez['title'].str.contains('A', case=False)) | (rez['title'].str.contains('B', case=False))].copy()

    # Remove rows with '.' for 'letter' value
    rez = rez[rez['letter'] != '.'].copy()

    # Sort dataframe by section, lessonid and user_id
    rez.sort_values(by=['section', 'lessonid', 'user_id'], inplace=True)

    # mapping true/false to p/n (pareizi/nepareizi)
    di = {'true': 'p', 'false': 'n'}
    rez.replace({'correct_answer': di}, inplace=True)

    # Convert everything to uppercase in case there are some in lowercase
    rez['letter'] = rez['letter'].str.upper()

    return rez


# Aggregate question pairs
def aggregator(x):
    a = x[(x['letter'].shift(-1) == 'B')].copy()
    b = x[(x['letter'] == 'B')].copy()
    ab = a.append(b, sort=True)
    ab.sort_values(by=['section', 'lessonid', 'user_id', 'letter'], inplace=True)
    ab.reset_index(inplace=True)
    ab.drop_duplicates(inplace=True)
    a = ab[(ab['letter'] == 'A')].copy()
    b = ab[(ab['letter'].shift(1) == 'A')].copy()
    ab = a.append(b, sort=True)
    ab.sort_values(by=['section', 'lessonid', 'user_id', 'letter'], inplace=True)
    ab.reset_index(inplace=True)
    ab.drop_duplicates(inplace=True)
    return ab


# Final aggregation and creation of figures
# coll -> column to visualise (sectionid | lessonid | user_id);
# x -> initial dataframe from loading; y -> ab question pair dataframe
def grouping_fig(coll, x, y):
    global temas, krasa, summa
    # Join 'p' and 'n' results into one column based on 'a' and 'b' questions. Keep lessonid number.
    # Convert to dataframe using to_frame
    x_df = y.groupby(by=[y.index // 2, coll])['correct_answer'].agg('-'.join).to_frame()
    # Reset index
    x_df.reset_index(level=[coll], inplace=True)

    if coll == 'sectionid':
        section_filter = x['type'].isin(['result'])
        result_df = x[['section', coll, 'type']]
        result_df = result_df[section_filter].drop_duplicates(subset=[coll]).drop(['type'], axis=1).copy()
        # create dictionary of section titles with corresponding contentid
        section_di = pd.Series(result_df.section.values, index=result_df.sectionid).to_dict()
        krasa = 'lightseagreen' #'mediumslateblue' lightseagreen saddlebrown
        x_df.replace({'sectionid': section_di}, inplace=True)

    if coll == 'lessonid':
        content_filter = x['type'].isin(['content'])
        content_df = x[['section', coll, 'title', 'type']]
        content_df = content_df[content_filter].drop_duplicates(subset=[coll]).drop(['type'], axis=1).copy()
        # create dictionary of lesson titles with corresponding lessonid
        lesson_di = pd.Series(content_df.title.values, index=content_df.lessonid).to_dict()
        krasa = 'lightseagreen' #'dodgerblue'
        x_df.replace({'lessonid': lesson_di}, inplace=True)

    if coll == 'user_id':
        krasa = 'lightseagreen' #'lightcoral'

    # Create final dataframe containing sum of all question pairs for each Unit (section)
    x_df = pd.crosstab(index=x_df[coll], columns=x_df['correct_answer'])

    # Create necessary column if they do not exist
    if 'n-n' not in x_df.columns:
        x_df['n-n'] = 0
    if 'n-p' not in x_df.columns:
        x_df['n-p'] = 0
    if 'p-p' not in x_df.columns:
        x_df['p-p'] = 0
    if 'p-n' not in x_df.columns:
        x_df['p-n'] = 0

    # Create column 'x-n' that is sum of 'n-n' and 'p-n' columns
    x_df['x-n'] = x_df['n-n'] + x_df['p-n']
    x_df.drop(columns=['n-n', 'p-n'], inplace=True)

    # Create column sum of all pairs per Unit
    x_df['sum'] = x_df['n-p'] + x_df['p-p'] + x_df['x-n']

    # Number of units
    if coll == 'sectionid':
        temas = len(x_df.index)

    # Sum of all question pairs
    summa = x_df['sum'].sum()

    # Create final values using average probability
    x_df['n-p'] = x_df['n-p'] / x_df['sum']
    x_df['p-p'] = x_df['p-p'] / x_df['sum']
    x_df['x-n'] = x_df['x-n'] / x_df['sum']
    x_df.drop(columns=['sum'], inplace=True)

    figure = go.Figure(data=[
        go.Mesh3d(
            x=df_tele['N-P'],
            y=df_tele['P-P'],
            z=df_tele['X-N'],
            color='steelblue',
            opacity=0.3,
            hoverinfo='none',
        ),
        go.Scatter3d(
            x=x_df['n-p'],
            y=x_df['p-p'],
            z=x_df['x-n'],
            mode="markers",
            text=x_df.index,
            hovertemplate='Piemērots: %{x:.2f}<br>Viegls: %{y:.2f}<br>Nepiemērots: %{z:.2f}<extra>%{text}</extra>',
            marker=dict(size=8, symbol="circle", color=krasa)  # color=student_df, colorscale='balance'
        ),
    ])

    figure.update_layout(
        scene_camera=camera,
        scene=dict(
            xaxis_title="N-P",
            yaxis_title="P-P",
            zaxis_title="X-N",
            xaxis=axis("rgb(200, 200, 230)"),
            yaxis=axis("rgb(230, 200,230)"),
            zaxis=axis("rgb(230, 230,200)"),
            annotations=[
                annotation(0.222, 0.111, 0.666, '<b>Nepiemērots</b>', 'center', 'indianred'),
                annotation(0.667, 0.333, 0, '<b>Piemērots</b>', 'right', 'mediumseagreen'),
                annotation(0, 1, 0, '<b>Viegls</b>', 'left', 'royalblue')
            ],
        ),
        height=700,
        margin=dict(
            r=0, l=0,
            b=0, t=0),
    )
    return figure


# APPLICATION LAYOUT
app.layout = html.Div([
    dbc.Row(
        dbc.Col([
            html.H1('ARTSS datu vizualizācija', className="text-center my-5"),
            html.Div(['''
                    Šajā tīmekļa lietotnē skolotājs var vizuāli novērot kursa satura piemērotību un efektivitāti 
                    izmantojot Telecīdas
                    ''',
                      dcc.Link(html.H6('ARTSS kursi', className='mt-3'), href='https://artss.mii.lv/',
                               target='_blank'),
                      ], className="text-center my-5"),
        ], width=8,
        ), justify='center',
    ),

    dbc.Row([
        dbc.Col([
            html.Div([html.H5('Diagramma'),
                      '''
                Vizualizācijas metodes nosaukums ir Telecīdas. Tā ir 3D diagramma, kur katrs punkts plaknē norāda uz 
                vienu no satura tēmām. Apmācamajam atbilstošs un efektīvs saturs ir tad, kad punkts atrodas tuvāk  
                trīsstūra kreisajam apakšējam stūrim.
                '''], className='shadow-sm ml-3 my-3 border p-3'
                     ),
            html.Div("Izvēlies kursu", className='ml-3'),
            dcc.Dropdown(options=dictionary,
                searchable=True,
                clearable=False,
                placeholder='Izvēlies vai ievadi kursa nosaukumu',
                persistence=True,
                persistence_type='memory',  # memory-tab refresh, session-tab is closed, local-cookies
                id='courses_dropdown',
                className='shadow-sm ml-3 mb-5'
            ),
            html.Div(
                [
                    html.Div([
                        html.H6('Satura piemērotības zonas'),
                        html.Img(title='paraugs', src='assets/landscape-segments.jpg', width='100%'),
                        dbc.Alert("Atbilstošs saturs", color="success", className='mb-0'),
                        dbc.Alert("Neatbilstošs saturs. Pārāk sarežģīts", color="danger", className='my-1'),
                        dbc.Alert("Daļēji neatbilstošs, pārāk viegls saturs. ", color="primary", className='mt-0'),
                    ], className='shadow-sm mb-3 border p-3'),
                ], className='ml-3'
            )
        ], width=3),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([
                        html.Div('Tēmas', className="card-title text-center"),
                        html.H1(id='tema', className='text-center clearfix')
                    ]), className=""
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.Div('Apakštēmas', className="card-title text-center"),
                        html.H1(id='pari', className='text-center')
                    ]), className=""
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.Div('Studenti', className="card-title text-center"),
                        html.H1(id='number_of_students', className='text-center')
                    ]), className=""
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.Div('Analizētie pāri', className="card-title text-center"),
                        html.H1(id='summa', className='text-center clearfix')
                    ]), className=""
                )
            ], className='shadow-sm mt-3 mb-3', style={'columnCount': 2}),
            dbc.Col([
                dcc.Loading(id="loading-2", children=[
                    html.Div(id="loading-output-2", style={'display': 'none'}),
                    dcc.Tabs([
                        dcc.Tab(label='Tēmas', children=[
                            dcc.Graph(
                                id='telecides-unit',
                                figure=fig,
                                config={'displaylogo': False, 'showTips': True}
                            )
                        ]),
                        dcc.Tab(label='Apakštēmas', children=[
                            dcc.Graph(
                                id='telecides-sub-unit',
                                figure=fig,
                                config={'displaylogo': False, 'showTips': True},
                            )
                        ]),
                        dcc.Tab(label='Studenti', children=[
                            dcc.Graph(
                                id='telecides-student',
                                figure=fig,
                                config={'displaylogo': False, 'showTips': True},
                            )
                        ]),
                    ]),
                ], type="default", fullscreen=False),
            ], className='shadow-sm border'),
        ], width=8),
    ], justify="center"),
    dbc.Row(
        dbc.Col(
            # html.H1('Papildus saturs'),
        ),
        justify='center'
    )
])


# ------------------- CALLBACKS ------------------------------------------------------------------
@app.callback(
    [Output(component_id='telecides-unit', component_property='figure'),
     Output(component_id='telecides-sub-unit', component_property='figure'),
     Output(component_id='telecides-student', component_property='figure'),
     Output(component_id='tema', component_property='children'),
     Output(component_id='number_of_students', component_property='children'),
     Output(component_id='pari', component_property='children'),
     Output(component_id='summa', component_property='children'),
     Output(component_id="loading-output-2", component_property='children')],
    [Input(component_id='courses_dropdown', component_property='value')]
)
def update_telecides(value):
    if value is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate

    df = loader(value)

    # Nested functions
    ab = aggregator(cleaner(df))

    # Number of question pairs
    pari = ab["lessonid"].nunique()
    # Number of students only
    number_of_students = ab["user_id"].nunique()

    fig1 = grouping_fig('sectionid', df, ab)
    fig2 = grouping_fig('lessonid', df, ab)
    fig3 = grouping_fig('user_id', df, ab)

    return fig1, fig2, fig3, temas, number_of_students, pari, summa, value


# -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
