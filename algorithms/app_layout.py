from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from algorithms import graph_formater
from config.courses_list import _courses


def layout():
    # create course list
    prefix = 'https://'
    base = 'artss.mii.lv/webservice/rest/server.php?courseid='
    token = '&wstoken=a78e76c2570f41a3f180d0979914c7dc'
    function = '&wsfunction=local_notifyemailsignup_functiongetstudentactivitydata&moodlewsrestformat=json'
    courses = _courses
    course_list = [
        {
            "label": f"{key}",
            "value": f"{prefix}{base}{value[0]}{token}{function}",
            "disabled": value[1]
        }
        for key, value in courses.items()
    ]

    # APPLICATION LAYOUT
    param = html.Div([
        html.Div([
            html.Img(src='../assets/eduaim-horiz.png',
                     style={'position': 'relative', 'width': '100%', 'top': '30px'}),
            html.Br(),
            html.Br(),
            html.H1(children='FOOD FOOTPRINT'),
            html.Label(
                'We are interested in investigating the food products that have the biggest impact on environment. \
                Here you can understand which are the products whose productions emit more greenhouse gases and \
                associate this with each supply chain step, their worldwide productions, and the water use.',
                style={'color': 'rgb(33 36 35)'})

        ], className='side_bar'),
        html.Div([
            html.Div([
                html.Div([
                    html.Label("Choose the Product's Origin:"),
                    html.Br(),
                    html.Br(),

                ], className='box', style={'margin': '10px', 'padding-top': '15px', 'padding-bottom': '15px'}),

                html.Div([
                    html.Div([

                        html.Div([
                            html.Label(id='title_bar'),
                            dcc.Graph(id='bar_fig'),
                            html.Div([
                                html.P(id='comment')
                            ], className='box_comment'),
                        ], className='box', style={'padding-bottom': '15px'}),

                        html.Div([
                            html.Img(style={'width': '100%', 'position': 'relative', 'opacity': '80%'}),
                        ]),

                    ], style={'width': '40%'}),

                    html.Div([

                        html.Div([
                            html.Label(id='choose_product', style={'margin': '10px'}),
                        ], className='box'),

                        html.Div([
                            html.Div([
                                html.Label('Emissions measured as kg of CO2 per kg of product',
                                           style={'font-size': 'medium'}),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Div([
                                        html.H4('Land use', style={'font-weight': 'normal'}),
                                        html.H3(id='land_use')
                                    ], className='box_emissions'),

                                    html.Div([
                                        html.H4('Animal Feed', style={'font-weight': 'normal'}),
                                        html.H3(id='animal_feed')
                                    ], className='box_emissions'),

                                    html.Div([
                                        html.H4('Farm', style={'font-weight': 'normal'}),
                                        html.H3(id='farm')
                                    ], className='box_emissions'),

                                    html.Div([
                                        html.H4('Processing', style={'font-weight': 'normal'}),
                                        html.H3(id='processing')
                                    ], className='box_emissions'),

                                    html.Div([
                                        html.H4('Transport', style={'font-weight': 'normal'}),
                                        html.H3(id='transport')
                                    ], className='box_emissions'),

                                    html.Div([
                                        html.H4('Packaging', style={'font-weight': 'normal'}),
                                        html.H3(id='packging')
                                    ], className='box_emissions'),

                                    html.Div([
                                        html.H4('Retail', style={'font-weight': 'normal'}),
                                        html.H3(id='retail')
                                    ], className='box_emissions'),
                                ], style={'display': 'flex'}),

                            ], className='box', style={'heigth': '10%'}),

                            html.Div([
                                html.Div([

                                    html.Div([
                                        html.Br(),
                                        html.Label(id='title_map', style={'font-size': 'medium'}),
                                        html.Br(),
                                        html.Label(
                                            'These quantities refer to the raw material used to produce the product selected above',
                                            style={'font-size': '9px'}),
                                    ], style={'width': '70%'}),
                                    html.Div([

                                    ], style={'width': '5%'}),
                                    html.Div([

                                        html.Br(),
                                        html.Br(),
                                    ], style={'width': '25%'}),
                                ], className='row'),

                                dcc.Graph(id='map', style={'position': 'relative', 'top': '-50px'}),

                                html.Div([

                                ], style={'margin-left': '15%', 'position': 'relative', 'top': '-38px'}),

                            ], className='box', style={'padding-bottom': '0px'}),
                        ]),
                    ], style={'width': '60%'}),
                ], className='row'),

                html.Div([
                    html.Div([
                        html.Label("3. Global greenhouse gas emissions from food production, in percentage",
                                   style={'font-size': 'medium'}),
                        html.Br(),
                        html.Label('Click on it to know more!', style={'font-size': '9px'}),
                        html.Br(),
                        html.Br(),
                        dcc.Graph()
                    ], className='box', style={'width': '40%'}),
                    html.Div([
                        html.Label("4. Freshwater withdrawals per kg of product, in Liters",
                                   style={'font-size': 'medium'}),
                        html.Br(),
                        html.Label('Click on it to know more!', style={'font-size': '9px'}),
                        html.Br(),
                        html.Br(),
                        dcc.Graph()
                    ], className='box', style={'width': '63%'}),
                ], className='row'),

                html.Div([
                    html.Div([
                        html.P(['GroupV', html.Br(),
                                'Ana Carrelha (20200631), Inês Melo (20200624), Inês Roque (20200644), Ricardo Nunes(20200611)'],
                               style={'font-size': '12px'}),
                    ], style={'width': '60%'}),
                    html.Div([
                        html.P(['Sources ', html.Br(),
                                html.A('Our World in Data', href='https://ourworldindata.org/', target='_blank'), ', ',
                                html.A('Food and Agriculture Organization of the United Nations',
                                       href='http://www.fao.org/faostat/en/#data', target='_blank')],
                               style={'font-size': '12px'})
                    ], style={'width': '37%'}),
                ], className='footer', style={'display': 'flex'}),
            ], className='main'),
        ]),
        #     html.Div([
        #         dbc.Row(
        #             dbc.Col([
        #                 html.H1('ARTSS datu vizualizācija', className="text-center my-5"),
        #                 html.Div(['''
        #                         Šajā tīmekļa lietotnē skolotājs var vizuāli novērot kursa satura piemērotību un efektivitāti
        #                         izmantojot Telecīdas
        #                         ''',
        #                           dcc.Link(html.H6('ARTSS kursi', className='mt-3'), href='https://artss.mii.lv/',
        #                                    target='_blank'),
        #                           ], className="text-center my-5"),
        #             ], width=8,
        #             ), justify='center',
        #         ),
        #
        #         dbc.Row([
        #             dbc.Col([
        #                 html.Div([html.H5('Diagramma'),
        #                           '''
        #                     Vizualizācijas metodes nosaukums ir Telecīdas. Tā ir 3D diagramma, kur katrs punkts plaknē norāda uz
        #                     vienu no satura tēmām. Apmācamajam atbilstošs un efektīvs saturs ir tad, kad punkts atrodas tuvāk
        #                     trīsstūra kreisajam apakšējam stūrim.
        #                     '''], className='shadow-sm ml-3 my-3 border p-3'
        #                          ),
        #                 html.Div("Izvēlies kursu", className='ml-3'),
        #                 dcc.Dropdown(options=course_list,
        #                              searchable=True,
        #                              clearable=False,
        #                              placeholder='Izvēlies vai ievadi kursa nosaukumu',
        #                              persistence=True,
        #                              persistence_type='memory',  # memory-tab refresh, session-tab is closed, local-cookies
        #                              id='courses_dropdown',
        #                              className='shadow-sm ml-3 mb-5'
        #                              ),
        #                 html.Div(
        #                     [
        #                         html.Div([
        #                             html.H6('Satura piemērotības zonas'),
        #                             html.Img(title='paraugs', src='../assets/landscape-segments.jpg', width='100%'),
        #                             dbc.Alert("Atbilstošs saturs", color="success", className='mb-0'),
        #                             dbc.Alert("Neatbilstošs saturs. Pārāk sarežģīts", color="danger", className='my-1'),
        #                             dbc.Alert("Daļēji neatbilstošs, pārāk viegls saturs. ", color="primary", className='mt-0'),
        #                         ], className='shadow-sm mb-3 border p-3'),
        #                     ], className='ml-3'
        #                 )
        #             ], width=3),
        #             dbc.Col([
        #                 dbc.CardGroup([
        #                     dbc.Card(
        #                         dbc.CardBody([
        #                             html.Div('Tēmas', className="card-title text-center"),
        #                             html.H1(id='num_units', className='text-center clearfix')
        #                         ]), className=""
        #                     ),
        #                     dbc.Card(
        #                         dbc.CardBody([
        #                             html.Div('Apakštēmas', className="card-title text-center"),
        #                             html.H1(id='num_sub', className='text-center')
        #                         ]), className=""
        #                     ),
        #                     dbc.Card(
        #                         dbc.CardBody([
        #                             html.Div('Studenti', className="card-title text-center"),
        #                             html.H1(id='num_students', className='text-center')
        #                         ]), className=""
        #                     ),
        #                     dbc.Card(
        #                         dbc.CardBody([
        #                             html.Div('Analizētie pāri', className="card-title text-center"),
        #                             html.H1(id='num_pairs', className='text-center clearfix')
        #                         ]), className=""
        #                     )
        #                 ], className='shadow-sm mt-3 mb-3', style={'columnCount': 2}),
        #                 dbc.Col([
        #                     dcc.Loading(id="loading-2", children=[
        #                         html.Div(id="loading-output-2", style={'display': 'none'}),
        #                         dcc.Tabs([
        #                             dcc.Tab(label='Tēmas', children=[
        #                                 dcc.Graph(
        #                                     id='telecides-unit',
        #                                     figure=graph_formater.fig,
        #                                     config={'displaylogo': False, 'showTips': True}
        #                                 )
        #                             ]),
        #                             dcc.Tab(label='Apakštēmas', children=[
        #                                 dcc.Graph(
        #                                     id='telecides-sub-unit',
        #                                     figure=graph_formater.fig,
        #                                     config={'displaylogo': False, 'showTips': True},
        #                                 )
        #                             ]),
        #                             dcc.Tab(label='Studenti', children=[
        #                                 dcc.Graph(
        #                                     id='telecides-student',
        #                                     figure=graph_formater.fig,
        #                                     config={'displaylogo': False, 'showTips': True},
        #                                 )
        #                             ]),
        #                         ]),
        #                     ], type="default", fullscreen=False),
        #                 ], className='shadow-sm border'),
        #             ], width=8),
        #         ], justify="center"),
        #         dbc.Row(
        #             dbc.Col(
        #                 # html.H1('Papildus saturs'),
        #             ),
        #             justify='center'
        #         )
        # ])
    ])
    return param
