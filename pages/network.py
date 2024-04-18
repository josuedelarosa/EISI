
from dash import Dash, html, dcc, callback, Output, Input
import networkx as nx
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from pyvis.network import Network
import json
import pandas as pd
from pathlib import Path

# Leer CSV siguiendo la arquitectura de carpetas
def read_csv_from_data(filename):
    current_path = Path(__file__)
    root_path = current_path.parent.parent
    csv_path = root_path / 'data' / filename
    return pd.read_csv(csv_path)

def inicializar_grafico(dfRA, dfMacro, dfMicro):
    nt = Network()

    # Agregar nodos de resultados de aprendizaje
    for index, row in dfRA.iterrows():
        title = row['Name'] + "\n" + "Descripción:" + row['Description'] + "\n" + "Profesor Líder:" + row["Profesor Líder"]
        nt.add_node(row['Name'], label=row['Name'], title=title, group=1, level=1, size=200)

    # Agregar nodos de macro competencias
    for index, row in dfMacro.iterrows():
        title = row['Id_macro'] + "\n" + row['Macro']
        nt.add_node(row['Id_macro'], label=row['Id_macro'], title=title, group=2, level=2, size=200)

    # Agregar nodos de micro competencias
    for index, row in dfMicro.iterrows():
        title = row['Id_micro'] + "\n" + row['Microcompetencia']
        nt.add_node(row['Id_micro'], label=row['Id_micro'], title=title, group=3, level=3, size=200)

    # Agregar relaciones entre macro competencias y resultados de aprendizaje
    for index, row in dfMacro.iterrows():
        rstApr = row['RA padre'].split(',')
        for ra in rstApr:
            nt.add_edge(row['Id_macro'], ra)

    # Agregar relaciones entre macro competencias y micro competencias
    for index, row in dfMicro.iterrows():
        nt.add_edge(row['Id_micro'], row['MacroCompetencias (MC)'])

    options = {
        "layout": {
            "hierarchical": {
                "direction": "LR",
                "levelSeparation": 8000,
                "nodeSpacing": 600,
                "treeSpacing": 400,
                "blockShifting": True,
                "edgeMinimization": True,
                "parentCentralization": True,
            },
            "improvedLayout": True
        },
        "physics": {
            "enabled": False
        },
        "edges": {
            "width": 20.0
        },
        "nodes": {
            "font": {
                "size": 130
            }
        }
    }

    nt.set_options(json.dumps(options))

    return nt

def filtro_curso(dfRA, dfMacro, dfMicro, cursos):
    ids_set = set(cursos)
    new_dfMicro = dfMicro[dfMicro['Id_micro'].isin(ids_set)]
    nt = Network()

    # Agregar nodos de resultados de aprendizaje
    for index, row in dfRA.iterrows():
        title = row['Name'] + "\n" + "Descripción:" + row['Description'] + "\n" + "Profesor Líder:" + row["Profesor Líder"]
        nt.add_node(row['Name'], label=row['Name'], title=title, group=1, level=1, size=200)

    # Agregar nodos de macro competencias
    for index, row in dfMacro.iterrows():
        title = row['Id_macro'] + "\n" + row['Macro']
        nt.add_node(row['Id_macro'], label=row['Id_macro'], title=title, group=2, level=2, size=200)

    # Agregar nodos de micro competencias
    for index, row in new_dfMicro.iterrows():
        title = row['Id_micro'] + "\n" + row['Microcompetencia']
        nt.add_node(row['Id_micro'], label=row['Id_micro'], title=title, group=3, level=3, size=200)

    # Agregar relaciones entre macro competencias y resultados de aprendizaje
    for index, row in dfMacro.iterrows():
        rstApr = row['RA padre'].split(',')
        for ra in rstApr:
            nt.add_edge(row['Id_macro'], ra)

    # Agregar relaciones entre macro competencias y micro competencias
    for index, row in new_dfMicro.iterrows():
        nt.add_edge(row['Id_micro'], row['MacroCompetencias (MC)'])

    options = {
        "layout": {
            "hierarchical": {
                "direction": "LR",
                "levelSeparation": 8000,
                "nodeSpacing": 600,
                "treeSpacing": 400,
                "blockShifting": True,
                "edgeMinimization": True,
                "parentCentralization": True,
            },
            "improvedLayout": True
        },
        "physics": {
            "enabled": False
        },
        "edges": {
            "width": 20.0
        },
        "nodes": {
            "font": {
                "size": 130
            }
        }
    }

    nt.set_options(json.dumps(options))

    return nt

dfMicro = read_csv_from_data('microCompetencias_updated-ALL_microCompetencias.csv')
dfMacro = read_csv_from_data('MacroCompetencias (MC)-all_options.csv')
dfRA = read_csv_from_data('ResultadosAprendizaje (RA)-Grid view.csv')
dfCursos = read_csv_from_data('CursosActual-Grid view.csv')



nt = inicializar_grafico(dfRA, dfMacro, dfMicro)

nt.height = '600px'
nt.save_graph("graph.html")

DIV_STYLE={
    "textAlign":"center",
    "backgroundColor": "#202c45",
    "color": "white",
    "marginLeft": "2rem",
    "marginRight": "2rem",
    "borderRadius": "1rem",
}


CONTROLS_STYLE={
    "marginLeft": "2rem",
    "marginRight": "2rem",
}
CUSTOM_IFRAME_STYLE = {
    "padding": "1rem",
    "overflowY": "hidden"
}

def drawControls():
    return html.Div([
        html.Div([
            html.P([
            html.Span("Controls"),
            ]),
        ],style=DIV_STYLE),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                id = "input_1",
                options=dfCursos["Nombre del Curso"],
                value='',
                placeholder='Curso',
            ),
            ]),
            dbc.Col([
                dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown-1')
            ]),
            dbc.Col([
                dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown-2')
            ]),
            

        ],style=CONTROLS_STYLE),
        html.Br(),
        
    ], style={"height":"25rem"})

# Definir el diseño de la aplicación Dash
def  layout():
    with open("graph.html", "r") as file:
        graph_html = file.read()
        
    return dbc.Card([
       dbc.Row([
           dbc.Col([
               html.Div([
                   dcc.Loading(html.Iframe(srcDoc=graph_html,id="network-graph", width='100%', height='650px', style=CUSTOM_IFRAME_STYLE)),
               ]),
               html.Br(),
               drawControls(),
               
           ])
       ])
        
    ])



    
