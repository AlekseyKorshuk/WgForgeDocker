import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dash import Dash, Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask

from modules.database.permanent import *

DATABASE_CONNECTION_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

# time.sleep(5)
engine = create_engine(DATABASE_CONNECTION_URI)
Session = sessionmaker(bind=engine, expire_on_commit=False)

server = Flask(__name__)
app = Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
Base = declarative_base()
from modules.database.classes import Book

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
from modules.core.controller import *
from modules.database.controller import *

add_default_datset()
dataframe = get_dataframe()
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


def attach_core_module():
    @app.callback(
        [Output("tbl", "data"), Output('tbl', 'columns'), Output('tbl_out', 'children')],
        [Input("button", "n_clicks")],
        [State("action", "value"), State("title", "value"), State("author", "value"), State("num_available", "value"), State("price", "value"), ]
    )
    def action_callback(n_clicks, action, title=None, author=None,
                 num_available=None, price=None):
        if title is not None and action is not None:
            try:
                if action == 'Add':
                    add_book(title, author, num_available, price)
                    result_string = "Item added!"
                else:
                    if delete_book(title, author):
                        result_string = "Item removed!"
                    else:
                        raise Exception("Not deleted")
            except Exception as ex:
                if action == 'Add':
                    result_string = "This book already exists!"
                else:
                    result_string = "This book does not exist!"
        else:
            result_string = ""

        dataframe = get_dataframe()
        return dataframe.to_dict('records'), [{"name": i, "id": i} for i in dataframe.columns], result_string
