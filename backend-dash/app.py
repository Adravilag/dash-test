import dash
import dash_mantine_components as dmc
from dash import html, dcc, Input, Output
from flask import jsonify
from flask_cors import CORS
import pandas as pd

from components.bar_charts import render_bar_chart
from components.pie_charts import render_category_pie
from components.line_charts import render_sales_evolution

df = pd.read_csv('data/ventas.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
CORS(server)

# ---------------------------------------------------------
# --- ENDPOINT API PARA ANGULAR ---
# ---------------------------------------------------------
@server.route('/api/ventas')
def get_ventas():
    data = df.to_dict(orient='records')
    return jsonify(data)

# ---------------------------------------------------------
# --- ESTILOS GLOBALES ---
# ---------------------------------------------------------
CONTENT_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",
    "justifyContent": "center",
    "width": "100%",
    "minHeight": "100vh",
    "padding": "2rem",
    "boxSizing": "border-box",
}

INNER_STYLE = {
    "width": "80%",
    "minHeight": "80vh",
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "center",
    "gap": "1.5rem",
}

LOADING_OVERLAY_STYLE = {
    "width": "100%",
    "flex": "1",
}

# ---------------------------------------------------------
# --- LAYOUT ---
# ---------------------------------------------------------
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light", "primaryColor": "indigo"},
    children=[
        dcc.Location(id="url", refresh=False),
        dmc.Container(
            fluid=True,
            p=0,
            m=0,
            style={"width": "100%", "maxWidth": "100%"},
            children=[
                dcc.Loading(
                    id="loading-wrapper",
                    type="default",
                    color="#4c6ef5",
                    children=html.Div(
                        id="page-content",
                        style=CONTENT_STYLE,
                        children=[
                            # El wrapper del 80% vive aquí, vacío al inicio
                            # Los callbacks lo rellenan via id="page-content"
                        ]
                    ),
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
    print(f"[NAV] path → '{path}'")

    routes = {
        "/ventas":     lambda: render_bar_chart(df),
        "/":           lambda: render_bar_chart(df),
        "":            lambda: render_bar_chart(df),
        "/categorias": lambda: render_category_pie(df),
        "/evolucion":  lambda: render_sales_evolution(df),
    }

    renderer = routes.get(path)
    content = renderer() if renderer else dmc.Alert(
        f"Ruta no reconocida: {path}",
        color="red",
        title="Error 404",
    )

    # Wrapper que centra visualmente el contenido al 80%
    return html.Div(
        content,
        style={
            "width": "80%",
            "minHeight": "80vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "margin": "0 auto",   # centra horizontalmente el bloque
        }
    )
    
if __name__ == "__main__":
    app.run(debug=True, port=8050)