import dash_mantine_components as dmc
from dash import dcc
import plotly.express as px

def render_bar_chart(df, x_axis='Producto', color_by='Categoria'):
    """
    Crea un gráfico de barras animado con Dash Mantine Components.
    """
    # 1. Procesamiento de datos
    df_grouped = df.groupby([x_axis, color_by])['Ventas'].sum().reset_index()
    
    # 2. Creación del gráfico
    fig = px.bar(
        df_grouped,
        x=x_axis,
        y='Ventas',
        color=color_by,
        barmode='group',
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={'Ventas': 'Euros (€)', x_axis: x_axis.capitalize()}
    )
    
    # 3. Ajustes de diseño y ANIMACIÓN
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        hovermode="x unified",
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        # --- CONFIGURACIÓN DE ANIMACIÓN ---
        transition_duration=800,
        transition_easing="back-out" # Un pequeño efecto de "rebote" al final
    )

    # 4. Retornamos el componente
    return dmc.Paper(
        children=[
            dmc.Group(
                children=[
                    dmc.Text(f"Análisis de Ventas por {x_axis}", fw=700, size="lg"),
                    dmc.Badge("Live", variant="dot", color="indigo"),
                ],
                justify="space-between",
                mb="md"
            ),
            dcc.Graph(
                figure=fig, 
                config={'displayModeBar': False},
                animate=True
            )
        ],
        withBorder=True,
        shadow="sm",
        p="lg",
        radius="md",
        className="animate-target", # Conexión con assets/style.css
        style={"backgroundColor": "#ffffff"}
    )