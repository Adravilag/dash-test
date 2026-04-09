import dash_mantine_components as dmc
from dash import dcc
import plotly.express as px

def render_category_pie(df):
    fig = px.pie(
        df, 
        values='Ventas', 
        names='Categoria',
        hole=0.4,
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # ESTO es lo que crea el efecto de "rellenado"
    fig.update_traces(
        textinfo='percent+label',
        # Permite que los sectores se animen al entrar
        insidetextorientation='radial',
        sort=False # Mantiene el orden para que la animación sea predecible
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        # Configuramos la transición para que sea circular
        transition_duration=1500, # Aumentamos a 1.5s para apreciar el "giro"
        transition_easing="cubic-in-out",
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center")
    )

    return dmc.Paper(
        children=[
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text("Distribución de Ingresos", fw=700, size="lg"),
                    dcc.Graph(
                        figure=fig, 
                        config={'displayModeBar': False},
                        style={"height": "350px"},
                        # IMPORTANTE: animate=True debe estar aquí
                        animate=True 
                    )
                ]
            )
        ],
        withBorder=True,
        shadow="sm",
        p="lg",
        radius="md",
        className="animate-target"
    )