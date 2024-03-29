from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from interface import graph_formater
from config.courses_list import _courses
from urllib.parse import urlparse, parse_qs


def layout():
    # create course list
    prefix = 'https://'
    # base = 'artss.mii.lv/webservice/rest/server.php?courseid='
    # token = '&wstoken=a78e76c2570f41a3f180d0979914c7dc'
    # function = '&wsfunction=local_notifyemailsignup_functiongetstudentactivitydata&moodlewsrestformat=json'

    base = 'eduaim.moodle.mii.lv/webservice/rest/server.php?courseid='
    token = '&wstoken=1cf6a9fcd683d94402b54f63e11760cd'
    function = '&wsfunction=local_eduaimdatamod_functiongetstudentactivitydata&moodlewsrestformat=json'
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
        html.Link(rel='icon', href='../assets/favicon.ico', type='image/x-icon'),
        # Banner ------------------------------------------------------------
        html.Div(
            [
                html.A(
                    [
                        html.Img(
                            src="/assets/img.png",
                            alt="eduaim"
                        ),
                    ],
                    href="#",
                    target='_blank',
                    className="logo-banner",
                ),
                html.Div(
                    [
                        html.A(
                            "Moodle",
                            href="https://eduaim.moodle.mii.lv/",
                            className="doc-link"
                        ),
                        html.A(
                            "EduAim",
                            href="https://www.eduaim.eu/",
                            className="doc-link"
                        ),
                    ],
                    className="navbar"
                ),
            ],
            className="banner",
        ),

        # Dropdown bar ------------------------------------------------------------
        html.Div(
            [

                html.H1('ZUM', className="text-center pb-0", style={"fontSize": "5rem"}),
                html.H1('Zināšanu uztveres monitorings', className="text-center pt-0 my-0 pb-3", style={"fontSize": "1.5rem"}),
                html.Div(['''
                    ZUM ir interaktīva datu vizualizācijas tīmekļa lietojumprogramma, kas galvenokārt paredzēta 
                    izglītības iestāžu akadēmiskajam personālam, piemēram, skolotājiem un lektoriem, lai analizētu un 
                    izprastu studentu sniegumu konkrētos kursos
                    ''',
                          ], className="text-center mb-5"),
                html.Div(
                    [
                        html.Img(
                            src='/assets/loupe.png',
                            className="loupe-img",
                        ),
                        dcc.Dropdown(options=course_list,
                                     searchable=True,
                                     clearable=False,
                                     placeholder='Izvēlies vai ievadi kursa nosaukumu',
                                     persistence=True,
                                     persistence_type='memory',
                                     # memory-tab refresh, session-tab is closed, local-cookies
                                     id='courses_dropdown',
                                     className='shadow-sm',
                                     ),
                    ],
                    className="search-bar",
                ),
            ],
            className="search-wrapper container"
        ),

        # Main content ----------------------------------------------------------


        dbc.Row([
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div('Tēmas', className="card-title text-center"),
                            html.H2(id='num_units', className='text-center clearfix bubble'),
                            html.Div(
                                "Kopējais tēmu skaits kursā",
                                className='hover-text',
                            ),
                        ]), className=""
                    ),
                    dbc.Card(
                        dbc.CardBody([
                            html.Div('Apakštēmas', className="card-title text-center"),
                            html.H2(id='num_sub', className='text-center bubble'),
                            html.Div(
                                "Kopējais apakštēmu skaits kursā",
                                className='hover-text',
                            ),
                        ]), className=""
                    ),
                    dbc.Card(
                        dbc.CardBody([
                            html.Div('Studenti', className="card-title text-center"),
                            html.H2(id='num_students', className='text-center bubble'),
                            html.Div(
                                "Kopējais analizēto studentu skaits kursā",
                                className='hover-text',
                            ),
                        ]), className=""
                    ),
                    dbc.Card(
                        dbc.CardBody([
                            html.Div('Analizētie pāri', className="card-title text-center"),
                            html.H2(id='num_pairs', className='text-center clearfix bubble'),
                            html.Div(
                                "Kopējais kursā analizēto jautājumu pāru skaits (ievadjautājums - pašpārbaudes jautājums)",
                                className='hover-text',
                            ),
                        ]), className=""
                    ),
                ], className='shadow-sm mt-3 mb-3', style={'columnCount': 2}),
                dbc.Col([
                    dcc.Loading(id="loading-2", children=[
                        html.Div(id="loading-output-2", style={'display': 'none'}),
                        dcc.Tabs([
                            dcc.Tab(label='Tēmas', children=[
                                html.H6('Punktu novietojusms pa tēmām', className="text-center mt-4"),
                                html.P('Cik piemērota, nepiemērota vai viegla ir katra no tēmām',
                                       className="mt-1 ml-3 graph-sub-text text-center"),
                                dcc.Graph(
                                    id='telecides-unit',
                                    figure=graph_formater.fig,
                                    config={'displaylogo': False, 'showTips': True}
                                ),
                            ],  className='custom-tab', selected_className='custom-tab--selected'),
                            dcc.Tab(label='Apakštēmas', children=[
                                html.H6('Punktu novietojusms pa apakštēmām', className="text-center mt-4"),
                                html.P('Cik piemērota, nepiemērota vai viegla ir katra no apakštēmām',
                                       className="mt-1 ml-3 graph-sub-text text-center"),
                                dcc.Graph(
                                    id='telecides-sub-unit',
                                    figure=graph_formater.fig,
                                    config={'displaylogo': False, 'showTips': True},
                                ),
                            ]),
                            dcc.Tab(label='Studenti', children=[
                                html.H6('Punktu novietojusms katram studentam', className="text-center mt-4"),
                                html.P(
                                    'Cik piemērots kurss ir bijis katram no studentiem individuāli. Studentus var atpazīt pēc id numura, kas tiek piešķirts Moodle',
                                    className="mt-1 ml-3 graph-sub-text text-center"),
                                dcc.Graph(
                                    id='telecides-student',
                                    figure=graph_formater.fig,
                                    config={'displaylogo': False, 'showTips': True},
                                ),
                            ]),
                        ]),
                    ], type="default", fullscreen=False),
                ], className='shadow-sm border'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            id='sub-unit-count',
                            config={'displaylogo': False, 'showTips': True}
                        ),
                    ], className='shadow-sm border m-3'),
                    dbc.Col([
                        dcc.Graph(
                            id='student-activity',
                            config={'displaylogo': False, 'showTips': True}
                        ),
                    ], className='shadow-sm border m-3 clearfix'),
                ], className='mt-3 clearfix'),
            ], width=8),
            dbc.Col([
                html.Div([html.H5('Diagramma'),
                          '''
                    Vizualizācijas metodes nosaukums ir Telecīdas. Tā ir 3D diagramma, kur katrs punkts plaknē norāda uz
                    vienu no satura tēmām. Apmācamajam atbilstošs un efektīvs saturs ir tad, kad punkts atrodas tuvāk
                    trīsstūra kreisajam apakšējam stūrim.
                    '''], className='shadow-sm ml-3 my-3 border p-3'
                         ),
                html.Div(
                    [
                        html.Div([
                            html.H6('Satura piemērotības zonas'),
                            html.Img(title='paraugs', src='../assets/landscape-segments.jpg', width='100%'),
                            dbc.Alert("Atbilstošs saturs", color="success", className='mb-0'),
                            dbc.Alert("Neatbilstošs saturs. Pārāk sarežģīts", color="danger", className='my-1'),
                            dbc.Alert("Daļēji neatbilstošs, pārāk viegls saturs. ", color="primary", className='mt-0'),
                        ], className='shadow-sm mb-3 border p-3'),
                    ], className='ml-3'
                )
            ], width=3),
        ], justify="center"),

        # ES Logo ----------------------------------------------------------------
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(title='ES', src='../assets/ES_logo.png', width='100%', className="img-fluid es-logo mb-3 mt-5"),
                ]),
            ], width=4),


            html.Div(['''
                    "Augstskolu digitālās kapacitātes celšana ar tiešsaistes mācību resursu un analītikas viedu integrāciju" 8.2.3.0/22/A/003 ESF (REACT-EU) 
                    ''',
                      ], className="text-center"),
            html.Div(['''
                    "Enhanced Digital Capacity for Universities by Smart Integration of On-Line Learning Resources and Analytics." 8.2.3.0/22/A/003 ESF (REACT-EU)
                    ''',
                      ], className="text-center mb-5"),
        ], justify="center", className="my-5"),

        # Footer ----------------------------------------------------------------
        html.Footer(
            [
                html.A(
                    [
                        "Built with ",
                        html.A("Plotly Dash", href="https://plotly.com/dash/", target="_blank")
                    ],
                ),
            ]
        ),
    ], className="app-layout",)
    return param
