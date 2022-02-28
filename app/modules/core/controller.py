from modules.database.controller import get_all_books, add_book
from modules.core import permanent
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd


def get_dataframe():
    dataset = {}
    for book in get_all_books():
        book = dict(book.__dict__)
        book.pop('_sa_instance_state')
        book.pop('id')
        for key in book.keys():
            if key not in dataset:
                dataset[key] = []
            dataset[key].append(book[key])
    return pd.DataFrame(dataset)


def add_default_datset():
    dataframe = pd.DataFrame(permanent.DEFAULT_DATASET)
    for index, row in dataframe.iterrows():
        try:
            add_book(**dict(row))
        except Exception as ex:
            print(ex)


def set_layout(app, dataframe):
    app.layout = dbc.Container([
        dbc.Label('Simple data visualization:'),
        dash_table.DataTable(dataframe.to_dict('records'), [{"name": i, "id": i} for i in dataframe.columns], id='tbl'),
        html.Br(),
        dcc.Input(id="title", value="Робинзон Крузо"),
        dcc.Input(id="author", value="Даниель Дефо"),
        dcc.Input(id="num_available", value="4"),
        dcc.Input(id="price", value="2700"),
        dcc.Dropdown(
            ['Add', 'Delete'],
            searchable=False,
            id="action"
        ),
        html.Button(
            ['Perform'],
            id='button'
        ),
        dbc.Alert(id='tbl_out'),
    ])
    return app
