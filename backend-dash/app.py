import dash
import dash_mantine_components as dmc
from dash import html, dcc, Input, Output
from flask import jsonify, Response
from flask_cors import CORS
import pandas as pd
import json

# --- IMPORTACIONES DE COMPONENTES ---
from components.bar_charts import render_bar_chart
from components.pie_charts import render_category_pie
from components.line_charts import render_sales_evolution
import components.histogram_charts as histogram_charts
import components.treemap_charts as treemap_charts

# 1. Configuración de datos y App
df = pd.read_csv('data/ventas.csv')

app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
    update_title=None  # Elimina el "Updating..." del título de la pestaña
)

# --- SOLUCIÓN DEFINITIVA PARA EL "LOADING..." ---
# Reescribimos el esqueleto HTML para ocultar el loader por defecto de Dash
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            /* Oculta el texto "Loading..." inicial y cualquier loader de callback */
            #_dash-loading-default, 
            ._dash-loading, 
            .dash-loading-callback {
                display: none !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.title = "Dashboard"
server = app.server
CORS(server)

# 2. DEFINICIÓN ÚNICA DE RUTAS (Fuente de verdad para API y Navegación)
DASHBOARD_CONFIG = [
    {"id": "ventas", "label": "Ventas por Producto", "path": "/ventas", "render": lambda: render_bar_chart(df)},
    {"id": "categorias", "label": "Categorías", "path": "/categorias", "render": lambda: render_category_pie(df)},
    {"id": "evolucion", "label": "Evolución", "path": "/evolucion", "render": lambda: render_sales_evolution(df)},
    {"id": "distribucion", "label": "Distribución", "path": "/distribucion", "render": lambda: histogram_charts.render_histogram_chart(df)},
    {"id": "jerarquia", "label": "Mapa de Inventario", "path": "/jerarquia", "render": lambda: treemap_charts.render_treemap_chart(df)},
]

# ---------------------------------------------------------
# --- ENDPOINTS API ---
# ---------------------------------------------------------

@server.route('/api/config')
def get_config():
    """Retorna la configuración de botones para Angular."""
    menu_data = {
        "dashboards": [
            {k: v for k, v in d.items() if k != 'render'} 
            for d in DASHBOARD_CONFIG
        ]
    }
    return Response(
        response=json.dumps(menu_data),
        status=200,
        mimetype='application/json'
    )

@server.route('/api/ventas')
def get_ventas():
    return jsonify(df.to_dict(orient='records'))

# ---------------------------------------------------------
# --- LAYOUT DASH ---
# ---------------------------------------------------------
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light", "primaryColor": "indigo"},
    children=[
        dcc.Location(id="url", refresh=False),
        dmc.Container(
            fluid=True, p=0, m=0,
            children=[
                html.Div(
                    id="page-content",
                    style={"width": "100%", "minHeight": "100vh", "padding": "2rem"}
                )
            ],
        ),
    ],
)

# ---------------------------------------------------------
# --- CALLBACK DE NAVEGACIÓN ---
# ---------------------------------------------------------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname: str):
    path = (pathname or "/").rstrip("/") or "/"
    
    # Buscamos el dashboard correspondiente
    match = next((d for d in DASHBOARD_CONFIG if d['path'] == path), None)
    
    if path == "/":
        content = DASHBOARD_CONFIG[0]['render']()
    elif match:
        content = match['render']()
    else:
        content = dmc.Alert(
            f"Ruta no reconocida: {path}",
            color="red",
            title="Error 404",
            variant="filled",
        )

    return html.Div(
        content,
        style={
            "width": "90%", # Un poco más ancho para aprovechar el espacio del iframe
            "minHeight": "80vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "margin": "0 auto",
        }
    )
    
if __name__ == "__main__":
    # Cambia debug=False si quieres probar la velocidad máxima de carga
    app.run(debug=True, port=8050)