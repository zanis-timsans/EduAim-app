import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)
users_to_drop = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 28, 31, 34,
                 36, 50, 55, 70, 73, 75, 119, 121, 235, 268]

def loader(api_url):
    api = api_url
    df2 = pd.read_json(api, orient="split")
    # Create 'user_role' column
    df1 = pd.DataFrame(df2['user'].values.tolist())
    df1.columns = 'user_' + df1.columns
    col = df2.columns.difference(['user'])
    df2 = pd.concat([df2[col], df1], axis=1)
    # Select only students
    df2 = df2[df2['user_roles'].apply(lambda x: ['student'] == x)]
    # Drop teaching staff user ids
    df2 = df2[~df2['user_id'].isin(users_to_drop)]

    return df2


# Clean and sort dataframe
# def cleaner(df):
#     # Select only rows with results value for type
#     rez = df[df["type"] == "result"]
#
#     # Filter out only first item in 'user_role'
#     rez = rez.loc[np.array(list(map(len, rez.user_roles.values))) == 1]
#
#     # Convert column from list to string
#     rez['user_roles'] = rez['user_roles'].apply(lambda z: ','.join(map(str, z)))
#
#     # Select only 'student' roles and make copy of original dataframe to avoid slicing view
#     rez = rez.loc[rez.user_roles == 'student'].copy()
#
#     # Transform time feature to datetime object
#     rez["datetime"] = pd.to_datetime(rez["datetime"])
#
#     # Keeping only first occurrence and dropping all other
#     rez = rez.drop_duplicates(subset=['user_id', 'itemid'], keep="first")
#
#     # Drop unnecessary columns
#     rez.drop(['id', 'answer', 'answer_submitted', 'question', 'timestamp', 'type', 'user_roles'], axis=1,
#              inplace=True)
#
#     # Convert everything to uppercase in case there are some in lowercase
#     rez['title'] = rez['title'].str.upper()
#
#     # Take last
#     rez['letter'] = rez['title'].str.strip().str[-1]
#
#     # Remove rows that are not a or b
#     rez = rez[(rez['title'].str.contains('A', case=False)) | (rez['title'].str.contains('B', case=False))].copy()
#
#     # Remove rows with '.' for 'letter' value
#     rez = rez[rez['letter'] != '.'].copy()
#
#     # Sort dataframe by section, lessonid and user_id
#     rez.sort_values(by=['section', 'lessonid', 'user_id'], inplace=True)
#
#     # mapping true/false to p/n (pareizi/nepareizi)
#     di = {'true': 'p', 'false': 'n'}
#     rez.replace({'correct_answer': di}, inplace=True)
#
#     # Convert everything to uppercase in case there are some in lowercase
#     rez['letter'] = rez['letter'].str.upper()
#
#     a = rez[(rez['letter'].shift(-1) == 'B')].copy()
#     b = rez[(rez['letter'] == 'B')].copy()
#     ab = a.append(b, sort=True)
#     ab.sort_values(by=['section', 'lessonid', 'user_id', 'letter'], inplace=True)
#     ab.reset_index(inplace=True)
#     ab.drop_duplicates(inplace=True)
#     a = ab[(ab['letter'] == 'A')].copy()
#     b = ab[(ab['letter'].shift(1) == 'A')].copy()
#     ab = a.append(b, sort=True)
#     ab.sort_values(by=['section', 'lessonid', 'user_id', 'letter'], inplace=True)
#     ab.reset_index(inplace=True)
#     ab.drop_duplicates(inplace=True)
#     return ab


def cleaner(x):
    # Filter to only "result" rows with a single "student" user role and drop Sections that are 'None'
    rez = x[(x["type"] == "result") &
            (x['lessonid'] != 0) &
            (x['section'].astype(str) != 'None')].copy()

    # Transform time feature to datetime object
    rez["datetime"] = pd.to_datetime(rez["datetime"])

    # Keeping only first occurrence and dropping all other
    rez = rez.drop_duplicates(subset=['user_id', 'itemid'], keep="first")

    # Drop unnecessary columns
    rez = rez.drop(columns=['id', 'answer', 'answer_submitted', 'question', 'timestamp', 'type', 'user_roles'])

    # Rename title to letter for better readability
    rez = rez.rename(columns={'title': 'letter'})

    # Convert title to uppercase and extract last letter
    rez['letter'] = rez['letter'].str.strip().str[-1]

    # Keep only rows with 'A' or 'B' in letter
    rez = rez[rez['letter'].str.contains('[AB]', case=False)]

    # Sort by section, lessonid, and user_id
    rez = rez.sort_values(by=['section', 'lessonid', 'user_id'])

    # Map "true" to "p" and "false" to "n" in correct_answer
    rez['correct_answer'] = rez['correct_answer'].replace({'true': 'p', 'false': 'n'})

    return rez


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
def group_dataframe(col, x, y):
    color = 'lightseagreen'
    subjects = ''
    # Join 'p' and 'n' results into one column based on 'a' and 'b' questions. Keep lessonid number.
    # Convert to dataframe using to_frame
    x_df = y.groupby(by=[y.index // 2, col])['correct_answer'].agg('-'.join).to_frame()
    # Reset index
    x_df.reset_index(level=[col], inplace=True)

    if col == 'sectionid':
        section_filter = x['type'].isin(['result'])
        result_df = x[['section', col, 'type']]
        result_df = result_df[section_filter].drop_duplicates(subset=[col]).drop(['type'], axis=1).copy()
        # create dictionary of section titles with corresponding contentid
        section_di = pd.Series(result_df.section.values, index=result_df.sectionid).to_dict()
        color = 'lightseagreen' #'mediumslateblue' lightseagreen saddlebrown
        x_df.replace({'sectionid': section_di}, inplace=True)

    if col == 'lessonid':
        content_filter = x['type'].isin(['content'])
        content_df = x[['section', col, 'title', 'type']]
        content_df = content_df[content_filter].drop_duplicates(subset=[col]).drop(['type'], axis=1).copy()
        # create dictionary of lesson titles with corresponding lessonid
        lesson_di = pd.Series(content_df.title.values, index=content_df.lessonid).to_dict()
        color = 'lightseagreen' #'dodgerblue'
        x_df.replace({'lessonid': lesson_di}, inplace=True)

    if col == 'user_id':
        color = 'lightseagreen' #'lightcoral'

    # Create final dataframe containing sum of all question pairs for each Unit (section)
    x_df = pd.crosstab(index=x_df[col], columns=x_df['correct_answer'])

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
    if col == 'sectionid':
        subjects = len(x_df.index)

    # Sum of all question pairs
    sum = x_df['sum'].sum()

    # Create final values using average probability
    x_df['n-p'] = x_df['n-p'] / x_df['sum']
    x_df['p-p'] = x_df['p-p'] / x_df['sum']
    x_df['x-n'] = x_df['x-n'] / x_df['sum']
    x_df.drop(columns=['sum'], inplace=True)

    return x_df, sum, subjects, color


# Create dataframe for visualising 'Complete learning acquisition landscape'
df_tele = pd.DataFrame(data=[['too complicated content', 0.222, 0.111, 0.666],
                             ['too easy content', 0, 1, 0, ],
                             ['ideally matching content', 0.667, 0.333, 0]],
                       columns=['content', 'N-P', 'P-P', 'X-N'], index=None)


def group_subunit_count(df):
    return df.groupby('sectionid').agg(
        skaits=('lessonid', 'nunique'),  # Count of unique sub-ids
        title=('section', 'first')  # Take the first 'name' within each group
    ).reset_index()

