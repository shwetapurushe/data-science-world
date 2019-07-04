import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']





# 1. APP Layout
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div(children = [
    html.H1(children= "How good is my train ? "),
    
    html.Div(children = '''
    This small app ties together my learning of Dash and NLP tokenization.
    ''')
]
)


# 2.  Server logic
if __name__ == '__main__':
    app.run_server(debug = True)

