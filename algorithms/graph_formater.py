import plotly.graph_objects as go
from algorithms import data_load_and_transformer


def format_annotation(x, y, z, text, anchor, color):
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
def format_axis(color):
    return dict(
        nticks=6, range=[0,1],
        backgroundcolor=color,
        gridcolor="white",
        showbackground=True,
        zerolinecolor="white",
        showspikes=False)


# Camera angle for the plot
camera = dict(
    eye=dict(x=2, y=2, z=0.8)
)


# Initial figure with the learning landscape and without 3d scatter
fig = go.Figure(data=[
    go.Mesh3d(
        x=data_load_and_transformer.df_tele['N-P'],
        y=data_load_and_transformer.df_tele['P-P'],
        z=data_load_and_transformer.df_tele['X-N'],
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
        xaxis=format_axis("rgb(200, 200, 230)"),
        yaxis=format_axis("rgb(230, 200,230)"),
        zaxis=format_axis("rgb(230, 230,200)"),
        annotations=[
            format_annotation(0.222, 0.111, 0.666, '<b>Nepiemērots</b>', 'center', 'indianred'),
            format_annotation(0.667, 0.333, 0, '<b>Piemērots</b>', 'right', 'mediumseagreen'),
            format_annotation(0, 1, 0, '<b>Viegls</b>', 'left', 'royalblue')
        ],
    ),
    height=600,
    margin=dict(
        r=0, l=0,
        b=0, t=0),
)


# def create_graph(df, color):
# TODO: create marker color as parameter based on column
def create_graph(col, df, pairs):
    group = data_load_and_transformer.group_dataframe(col, df, pairs)[0]
    figure = go.Figure(data=[
        go.Mesh3d(
            x=data_load_and_transformer.df_tele['N-P'],
            y=data_load_and_transformer.df_tele['P-P'],
            z=data_load_and_transformer.df_tele['X-N'],
            color='steelblue',
            opacity=0.3,
            hoverinfo='none',
        ),
        go.Scatter3d(
            x=group['n-p'],
            y=group['p-p'],
            z=group['x-n'],
            mode="markers",
            text=group.index,
            hovertemplate='Piemērots: %{x:.2f}<br>Viegls: %{y:.2f}<br>Nepiemērots: %{z:.2f}<extra>%{text}</extra>',
            marker=dict(size=8, symbol="circle", color='lightseagreen')  # color=student_df, colorscale='balance'
        ),
    ])

    figure.update_layout(
        scene_camera=camera,
        scene=dict(
            xaxis_title="N-P",
            yaxis_title="P-P",
            zaxis_title="X-N",
            xaxis=format_axis("rgb(200, 200, 230)"),
            yaxis=format_axis("rgb(230, 200,230)"),
            zaxis=format_axis("rgb(230, 230,200)"),
            annotations=[
                format_annotation(0.222, 0.111, 0.666, '<b>Nepiemērots</b>', 'center', 'indianred'),
                format_annotation(0.667, 0.333, 0, '<b>Piemērots</b>', 'right', 'mediumseagreen'),
                format_annotation(0, 1, 0, '<b>Viegls</b>', 'left', 'royalblue')
            ],
        ),
        height=700,
        margin=dict(
            r=0, l=0,
            b=0, t=0),
    )
    return figure

