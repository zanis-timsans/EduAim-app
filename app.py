# -*- coding: utf-8 -*-

# visit http://127.0.0.1:8050/ in your web browser.

# Load libraries
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from algorithms import data_load_and_transformer as dlt
from interface import app_layout, graph_formater as grf

# Styles - CERULEAN (!), COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA (!),
# MINTY, PULSE (!), SANDSTONE (!), SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB (!), SUPERHERO, UNITED (!), YETI (!)
external_stylesheets = [dbc.themes.PULSE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,  # , external_stylesheets=external_stylesheets
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet': '“UTF-8”'}])

server = app.server

app.title = "ZUM"

# APPLICATION LAYOUT
app.layout = app_layout.layout()

# ------------------- CALLBACKS ------------------------------------------------------------------
@app.callback([
    Output(component_id='telecides-unit', component_property='figure'),
    Output(component_id='telecides-sub-unit', component_property='figure'),
    Output(component_id='telecides-student', component_property='figure'),
    Output(component_id="sub-unit-count", component_property='figure'),
    Output(component_id="student-activity", component_property='figure'),
    Output(component_id='num_units', component_property='children'),
    Output(component_id='num_sub', component_property='children'),
    Output(component_id='num_students', component_property='children'),
    Output(component_id='num_pairs', component_property='children'),
    Output(component_id="loading-output-2", component_property='children'),
    ],
    [
        Input(component_id='courses_dropdown', component_property='value'),
     ],
)
def update_telecides(value):
    """
    Load, clean, and visualize data from a Telecides dataset.

    Parameters:
    value (str): The filename of the dataset to load.

    Returns:
    A tuple containing the following items:
    - fig_sectionid: A plotly figure showing the distribution of section IDs.
    - fig_lessonid: A plotly figure showing the distribution of lesson IDs.
    - fig_user_id: A plotly figure showing the distribution of user IDs.
    - subjects: A pandas DataFrame containing the counts of each subject.
    - num_students: An integer representing the number of unique students.
    - num_pairs: An integer representing the number of unique lesson pairs.
    - sum: A pandas DataFrame containing the sum of watch_time for each section.
    - value (str): Webhook URL.
    """
    if value is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate

    # Load and clean data
    df = dlt.loader(value)
    cleaned_df = dlt.cleaner(df)
    print(cleaned_df)
    agg_df = dlt.aggregator(cleaned_df)

    # Create figures
    fig_sectionid = grf.create_telecides('sectionid', df, agg_df)
    fig_lessonid = grf.create_telecides('lessonid', df, agg_df)
    fig_user_id = grf.create_telecides('user_id', df, agg_df)

    fig_subunit_count = grf.create_subunit_count(df)
    fig_student_activity = grf.create_student_activity(df)

    # Compute summary statistics
    num_sub = cleaned_df['lessonid'].nunique()
    num_students = cleaned_df['user_id'].nunique()
    num_units, num_pairs = dlt.group_dataframe('sectionid', df, cleaned_df)[1:3]

    return fig_sectionid, \
           fig_lessonid, \
           fig_user_id, \
           fig_subunit_count, \
           fig_student_activity, \
           num_pairs, \
           num_sub, \
           num_students, \
           num_units, \
           value


# -------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
