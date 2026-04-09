import dash_mantine_components as dmc
from dash import dcc
import plotly.express as px

def render_sales_evolution(df):
    df_daily = df.groupby('Fecha')['Ventas'].sum().reset_index()

    fig = px.line(
        df_daily,
        x='Fecha',
        y='Ventas',
        markers=True,
        template='plotly_white',
        color_discrete_sequence=['#4c6ef5'],
        labels={'Ventas': 'Total Ventas (€)', 'Fecha': 'Día'}
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8, symbol='circle', line=dict(width=2, color='white')),
        connectgaps=True
    )

    fig.update_layout(
        # autosize=True es clave — deja que el contenedor dicte el tamaño
        autosize=True,
        margin=dict(l=10, r=10, t=20, b=10),
        hovermode="x unified",
        font=dict(family="Inter, sans-serif", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        transition_duration=800,
        transition_easing="exp-in-out",
        # Fondo transparente para que el Paper de Mantine se vea limpio
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return dmc.Paper(
        children=[
            dmc.Stack(
                gap="xs",
                children=[
                    dmc.Text("Evolución Temporal", fw=700, size="lg"),
                    dmc.Text(
                        "Tendencia de ingresos diarios acumulados",
                        size="sm",
                        c="dimmed",
                        mb="md"
                    ),
                    dcc.Graph(
                        figure=fig,
                        config={'displayModeBar': False},
                        animate=True,
                        # responsive=True + style width hacen el trabajo real
                        responsive=True,
                        style={"width": "100%", "minHeight": "400px"},
                    )
                ]
            )
        ],
        withBorder=True,
        shadow="sm",
        p="lg",
        radius="md",
        # Paper ocupa todo el ancho del contenedor padre
        style={"width": "100%"},
        className="animate-target",
    )