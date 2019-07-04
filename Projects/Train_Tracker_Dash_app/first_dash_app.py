import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']





# 1. APP Layout
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
        
        dcc.Graph(
            id='bc',
            
            figure={
                
                #1. 
                'data' : [
                    {'x': ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"], 
                     'y': [4, 1, 2, 6, 0,0,9], 'type': 'bar', 'name': 'SF'},
                ], # TODO put train timings here 
                
                #2. 
                'layout' : {
                    'title' : 'Delays of the Lowell Commuter rail across a week',
                    'xaxis':{
                        'title':'Days of the week'
                    },
                    'yaxis':{
                     'title':'Number of delays'
                    }
                }
                
                
            }# Figure ends
        )
    ]# layout
)


# 2.  Server logic
if __name__ == '__main__':
    app.run_server(debug = True)

