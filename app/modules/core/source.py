from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dash import Dash, Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask

from modules.database.permanent import *

DATABASE_CONNECTION_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

import time

time.sleep(5)  # allow docker to up database
engine = create_engine(DATABASE_CONNECTION_URI)
Session = sessionmaker(bind=engine, expire_on_commit=False)

server = Flask(__name__)
app = Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
Base = declarative_base()
from modules.database.classes import Book

while True:
    try:
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        break
    except:
        print('Waiting for database to be up...')
from modules.core.controller import *
from modules.database.controller import *

add_default_datset()
dataframe = get_dataframe()
app = set_layout(app, dataframe)


def attach_core_module():
    @app.callback(
        [Output("tbl", "data"), Output('tbl', 'columns'), Output('tbl_out', 'children')],
        [Input("button", "n_clicks")],
        [State("action", "value"), State("title", "value"), State("author", "value"), State("num_available", "value"),
         State("price", "value"), ]
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
