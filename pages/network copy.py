
from dash import Dash, html, dcc, callback, Output, Input
import networkx as nx
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from pyvis.network import Network
import json
import pandas as pd


dfMicro = pd.read_csv('data\microCompetencias_updated-ALL_microCompetencias.csv')
dfMacro = pd.read_csv('data\MacroCompetencias (MC)-all_options.csv')
dfRA =pd.read_csv( 'data\ResultadosAprendizaje (RA)-Grid view.csv')
dfCursos = pd.read_csv( 'data\CursosActual-Grid view.csv')



nt = Network()

#Agregamos los nodos de los resultados de aprendizaje 
for index, row in dfRA.iterrows():
    title = row['Name'] + "\n" + "Descripción:" +row['Description'] + "\n"+ "Profesor Líder:" + row["Profesor Líder"]

    nt.add_node(row['Name'], label=row['Name'], title=title , group=1, level=1, size=200 )
    
#Agregamos los nodos de macro competencias 
for index, row in dfMacro.iterrows():
    title = row['Id_macro']+ "\n" + row['Macro']
    nt.add_node(row['Id_macro'], label=row['Id_macro'], title=title, group=2, level=2,  size=200)

#Agregamos los nodos de micro competencias 
for index, row in dfMicro.iterrows():
    title = row['Id_micro'] + "\n" + row['Microcompetencia']
    nt.add_node(row['Id_micro'], label=row['Id_micro'], title=title, group=3, level=3,  size=200)

#Agregamos las relacion entre macro competencias y resultado de aprendizaje  
for index, row in dfMacro.iterrows():
    rstApr= row['RA padre'].split(',')
    for ra in rstApr:
        nt.add_edge(row['Id_macro'], ra)

#Agregamos las relacion entre macro competencias y micro competencias 
for index, row in dfMicro.iterrows():
    nt.add_edge(row['Id_micro'],row['MacroCompetencias (MC)'])

#neighbor_map = nt.get_adj_list()
 
                

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
        "width": 20.0  # Ajusta el grosor de las aristas aquí
    },
    "nodes": {
        "font": {
            "size": 130  # Ajusta el tamaño de la fuente de las etiquetas aquí
        }
    }
    
}

nt.set_options(json.dumps(options))




# nt = Network()

# # Agregar nodos
# nt.add_node(1)
# nt.add_node(2)
# nt.add_node(3)
# nt.add_node(4)
# nt.add_node(5)
# nt.add_node(6)
# nt.add_node(7)

# # Agregar aristas
# nt.add_edge(1, 2)
# nt.add_edge(1, 3)
# nt.add_edge(2, 4)
# nt.add_edge(2, 5)
# nt.add_edge(3, 6)
# nt.add_edge(3, 7)

# # Configurar opciones de visualización
# options = {
#     "layout": {
#         "hierarchical": {
#             "direction": "LR",
#             "levelSeparation": 200
#         }
#     },
#     "physics": {
#         "enabled": False
#     }
# }
# nt.set_options(json.dumps(options))


# # Create an instance of the Pyvis network
# g = Network()
# g.add_nodes([1,2,3], value=[10, 100, 400],
#             title=['I am node 1', 'node 2 here', 'and im node 3'],
#             x=[21.4, 54.2, 11.2],
#             y=[100.2, 23.54, 32.1],
#             label=['NODE 1', 'NODE 2', 'NODE 3'],
#             color=['#00ff1e', '#162347', '#dd4b39'])

# # Save the network as an HTML file
# #net.show_buttons(filter_=['nodes', 'edges', 'physics'])


# g.height = '400px'
# g.save_graph("graph.html")

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
        
    ], style={"height":"7rem"})

#, width='100%', height='645px', style=CUSTOM_IFRAME_STYLE
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



    
