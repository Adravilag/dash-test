import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, callback # <--- Importante usar 'callback'
import plotly.express as px
import pandas as pd

def render_histogram_chart(df):
    # Generamos el layout inicial
    return dmc.Paper(
        withBorder=True, shadow="sm", p="lg", radius="md",
        children=[
            dmc.Group(
                justify="space-between", mb="md",
                children=[
                    dmc.Text("Distribución de Ventas", fw=700),
                    dmc.SegmentedControl(
                        id="percentile-toggle", # ID EXACTO
                        data=[
                            {"value": "none", "label": "Solo Histograma"},
                            {"value": "basic", "label": "Mediana"},
                            {"value": "all", "label": "Todos"},
                        ],
                        value="all", # Valor inicial
                    ),
                ]
            ),
            dcc.Graph(id="histogram-percentile-graph") # ID EXACTO
        ]
    )

# ESTE CALLBACK DEBE ESTAR FUERA DE LA FUNCIÓN
@callback(
    Output("histogram-percentile-graph", "figure"),
    Input("percentile-toggle", "value"),
)
def update_graph(view_mode):
    # Forzamos lectura para debug
    df_internal = pd.read_csv('data/ventas.csv')
    
    fig = px.histogram(df_internal, x='Ventas', nbins=30, template='plotly_white', opacity=0.7, color_discrete_sequence=['#CED4DA'])
    
    stats = {
        "Mediana": df_internal['Ventas'].median(),
        "P75": df_internal['Ventas'].quantile(0.75),
        "P95": df_internal['Ventas'].quantile(0.95)
    }
    
    lines = []
    if view_mode == "basic": lines = ["Mediana"]
    elif view_mode == "all": lines = ["Mediana", "P75", "P95"]
    
    colors = {"Mediana": "#4C6EF5", "P75": "#FAB005", "P95": "#FA5252"}
    
    for label in lines:
        fig.add_vline(x=stats[label], line_dash="dash", line_color=colors[label], 
                      annotation_text=f"{label}: {stats[label]:.0f}€")
    
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), uirevision='constant') # uirevision evita que el zoom se resetee
    return fig