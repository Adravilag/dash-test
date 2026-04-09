# Este archivo convierte la carpeta en un módulo de Python
# y centraliza las importaciones de tus gráficas.

from .bar_charts import render_bar_chart
from .pie_charts import render_category_pie
from .line_charts import render_sales_evolution

# Esto permite que en app.py solo hagas: 
# from components import render_bar_chart, render_category_pie...