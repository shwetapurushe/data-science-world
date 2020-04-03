import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd;

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# **** Data preprocessing ***** 




#BAR CHART INFO
#one series
trace1 = go.Bar(
    x = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"], 
    y = [4, 1, 2, 6, 0,0,9],
    name ='train_bc'
)


layout = go.Layout(
    xaxis = {'title':'Days of the week'},
    yaxis = {'title':'Number of delays'},
    title ='Delays of the Lowell Commuter rail across a week'
)

data = [trace1]
figure = go.Figure(data = data, layout=layout)

#**************BAR CHART INFO













# APP STUFF
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
colors = {
    'text': '#FF7F0E'
}

app.layout = html.Div(children = [
    
        html.H1("How good is my train ? ", style={
            'textAlign':'center',
            'color' :colors['text']
        }),

    
    
        html.Div(children = '''
        This small app ties together my learning of Dash and NLP tokenization.
        ''',
                 style={
                     'textAlign':'center',
                     'color' :colors['text']
                 }
        ),
    
        
        #VIZ
        #THE TWO GRAPHS 
        html.Div([
            
            html.Div([
                dcc.Graph(id='bc',figure=figure)
            ], className = 'six columns'),
            
            html.Div([
                dcc.Graph(id='bc2',figure=figure)
            ],className = 'six columns')
            
        ], className="row")
    ]
)







# 2.  Server logic
if __name__ == '__main__':
    app.run_server(debug = True)