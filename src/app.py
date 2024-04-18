from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import sys
from pathlib import Path
#from pages import network
from pyvis.network import Network
import json

root_path = Path(__file__).parent.parent
pages_path = root_path / 'pages'
sys.path.append(str(pages_path))
import network


#from pages.network import nt

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = 'Reforma EISI'

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
    "height": "calc(100vh - 62.5px)",  # Agrega la altura para ocupar toda la ventana
    "overflowY": "scroll",
    "marginTop": "62.5px",
}

NAVBAR_STYLE={
    "marginRight": "6rem",

}

MENU_STYLE = {    
    "marginLeft": "1rem",
}

FOTTER_STYLE ={
    "backgroundColor": "#202c45",
    "color": "white",
    "textAlign": "center",
    "fontSize": "12px"
}

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="/#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="1"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
            style=NAVBAR_STYLE,
        ),
    ],
    brand= dbc.Row([
        dbc.Col([
            html.A(html.Img(src='assets/static/logoEscuela.png', height='35px', id="btn_sidebar"), style= MENU_STYLE),
        ]),
        dbc.Col([
            dbc.Col(dbc.NavbarBrand("Reforma EISI 2023", className="ms-2")),
        ])
    ]),
    brand_href="http://cormoran.uis.edu.co/eisi/",
    color="#202c45",
    dark=True,
    fluid=True,
    style={"position": "fixed", "top": 0, "width": "100%", "zIndex": 9999}
    
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

footer= html.Div([
    html.Footer("Copy © 2023 | Todos los derechos reservados.", style=FOTTER_STYLE)
], style={"position": "fixed", "bottom": 0, "width": "100%", "zIndex": 9999})

app.layout = html.Div([
    dcc.Location(id="url"),
    content,
    navbar,     
    footer
    
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def renderConten(pathname):
    if pathname == "/":
        return network.layout()

@app.callback(
    Output("network-graph","srcDoc"),
    [Input("input_1","value")]
)
def filtroCurso(value):
    if value:
        idCurso=network.dfCursos[network.dfCursos["Nombre del Curso"]==value]["CursosActual_ID"].to_string(index=False)
        idsMicro=network.dfMicro[network.dfMicro["CursosActual"]==idCurso]["Id_micro"]

        nt = network.filtro_curso(network.dfRA, network.dfMacro, network.dfMicro,idsMicro)

        nt.height = '600px'
        nt.save_graph("graph.html")

        with open("graph.html", "r") as file:
            graph_html = file.read()
        return graph_html
    else:
        nt =network.inicializar_grafico(network.dfRA, network.dfMacro, network.dfMicro)
        nt.height = '600px'
        nt.save_graph("graph.html")
        with open("graph.html", "r") as file:
            graph_html = file.read()
        return graph_html



if __name__ == '__main__':
    app.run_server(debug=True)