import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

def render_treemap_chart(df):
    """
    Renderiza un TreeMap para análisis de jerarquía (Categoría > Producto)
    """
    return dmc.Paper(
        withBorder=True, shadow="sm", p="lg", radius="md",
        style={"backgroundColor": "#ffffff"},
        children=[
            dmc.Group(
                justify="space-between", mb="md",
                children=[
                    dmc.Stack(
                        gap=0,
                        children=[
                            dmc.Text("Distribución Jerárquica de Inventario", fw=700, size="lg"),
                            dmc.Text("Tamaño basado en volumen de ventas", size="xs", c="dimmed"),
                        ]
                    ),
                    dmc.SegmentedControl(
                        id="treemap-value-selector",
                        data=[
                            {"value": "Ventas", "label": "Por Ingresos (€)"},
                            {"value": "Cantidad", "label": "Por Unidades"},
                        ],
                        value="Ventas",
                        color="indigo",
                    ),
                ]
            ),
            dcc.Graph(
                id="treemap-graph",
                config={'displayModeBar': False}
            )
        ],
    )

@callback(
    Output("treemap-graph", "figure"),
    Input("treemap-value-selector", "value")
)
def update_treemap(value_col):
    # 1. Cargar datos
    df_internal = pd.read_csv('data/ventas.csv')
    
    # IMPORTANTE: Verifica que 'Cantidad' exista en tu CSV. 
    # Si en el CSV se llama 'Unidades', cámbialo aquí o en el SegmentedControl.
    if value_col not in df_internal.columns:
        print(f"ERROR: La columna {value_col} no existe en el dataset")
        value_col = 'Ventas' # Fallback de seguridad

    # 2. Crear el gráfico
    fig = px.treemap(
        df_internal, 
        path=[px.Constant("Empresa"), 'Categoria', 'Producto'], 
        values=value_col, # Aquí es donde daba el error 500
        color='Ventas', 
        color_continuous_scale='RdYlBu',
        template='plotly_white'
    )

    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        uirevision='constant' # Evita que el gráfico parpadee al cambiar el filtro
    )

    return fig