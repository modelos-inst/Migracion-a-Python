#Librerías para ejecutar el dash
import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output

#Librería para graficar
import plotly.graph_objs as go

#Este comando importa todas las funciones del archivo Funciones.py
## El archivo Funciones.py se debe encontrar en la misma carpeta que este documento.
from Funciones import *

#Enlace a la hoja de estilos CSS y permite construir la herramiente Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Se crea el objeto app, dentro del cual se extrae el atributo server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Definir la interfaz de la aplicación
app.layout = html.Div([
    # titulo de la aplicación
    html.H1('Aplicación Políticas de Inventario', style={'textAlign': 'center'}),

    #Se realiza la división de recuadros entre el título y los demás objetos
    html.Div([
    #imprimir gráfica de costos
    dcc.Graph(id='Graf_Cost_Tot'),

    #Crear objeto para ingresar parametro de tasa de demanda con un control deslizante
    dcc.Slider(
            id = 'TasaDemanda',
            min = 0,
            max = 30,
            value = 15,
            step = 1
        ),
    
    #Crear objeto para especificar la tasa seleccionada por el usuario y las unidades
    html.Div(id='valorSlider')
    ])
])

@app.callback(
    #Outputs que se van a modificar cuando el usuario interactua
    [Output('Graf_Cost_Tot', 'figure'),
     Output('valorSlider', 'children')],
     #Input en el que se va a fijar el callback
    [Input('TasaDemanda', 'value')])
def update_graph(Tasa):
    #Importamos la información de la funcion en Funciones.py
    InfoCostos = Shiny_function(Tasa)

    #__________Generar gráfica de los costos para las próximas 10 semanas__________
   #cada variable trace guardada es una nueva curva a la gráfica
    trace1 = go.Scatter(
    x=InfoCostos['numero_semana'],
    y=InfoCostos['costo_semanal_PolActual'],
    mode='lines+markers',
    name='P Actual'
    )

    trace2 = go.Scatter(
    x=InfoCostos['numero_semana'],
    y=InfoCostos['costo_semanal_PolNueva'],
    mode='lines+markers',
    name='P nueva'
    )

    layout = go.Layout(
    title='Costo por política en las próximas semanas',
    xaxis=dict(title='Semana'),
    yaxis=dict(title='Costo')
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)

    return fig, f'Tasa seleccionada: {Tasa} cajas/semana'



if __name__ == '__main__':
    app.run_server(debug=True)





