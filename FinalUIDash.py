# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 13:40:41 2021

@author: rania
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:32:15 2021

@author: rania
"""


# Importing the libraries
import pickle
import pandas as pd
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px
import numpy as np

data = pd.read_csv(r"etsypredictedreviews.csv")



labels = ["Positive","Negative"]

scrape = pd.read_csv(r"scrappedReviews.csv")
scrape.head()
 
graph = px.pie(data_frame=data,values=[data['predictedvalue'].value_counts()[1],data['predictedvalue'].value_counts()[0]],
               names=['Positive Reviews','Negative Reviews'],
               color=['Positive Reviews','Negative Reviews'],
               color_discrete_sequence=['purple','red'],width=500,height=380,hole=0.5, )     
 
 
app = dash.Dash()
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


project_name = "Sentiments Analysis"

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def load_model():
    global pickle_model
    global vocab
    global scrappedReviews
    
    
    scrappedReviews = pd.read_csv('scrappedReviews.csv')
    
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    file = open("feature.pkl", 'rb') 
    vocab = pickle.load(file)
        
def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)

def create_app_ui():
    global project_name
    main_layout = dbc.Container(
        dbc.Jumbotron(
                [
                    
                    html.H1(id = 'heading', children = project_name, className = 'display-6 mb-4',style={'padding':5,'backgroundColor':'#e7696f'}),
                    html.Div([html.H1('Word Cloud'), dbc.Button("ALL Words",id="allbt",outline=True, color="info",className="mr-7", n_clicks_timestamp=0,style={'padding':'10px','padding-right':'15px','padding-left':'15px'}),
               
                   dbc.Button("Positve Words",id="posbt",outline=True, color="success", className="mr-1", n_clicks_timestamp=0, style={'padding':'15px','padding-right':'15px','padding-left':'15px'}),
              
                  dbc.Button("Negative Words", id="negbt", outline=True,color="danger",className="mr-1",n_clicks_timestamp=0,style={'padding':'10px','padding-right':'15px','padding-left':'15px'}), 
                
               
                html.Div(id='wordc',style={'padding':'15px'})
             
        ], style={'textAlign': 'Center'}),
                    html.Div([html.H1(children='Distribution of Positive and Negative Reviews', id='pieh1',style={'padding':5,'backgroundColor':'#e97f84'})]),
            #dcc.Graph(figure = graph, style={'width': '600','height':400,},className = 'd-flex justify-content-center'),
                                dcc.Graph(figure = graph,id='pie',className = 'd-flex justify-content-center'),
                                html.Br(),html.Hr(),html.Br(),
            html.Div([html.H1(children='Please enter your reviews for the product', id='dropdown_h1',style={'padding':5})],style={'backgroundColor':'#d6758d','height': 60}),
            html.Br(),html.Br(),
                    dbc.Textarea(id = 'textarea', className="mb-3", placeholder="Enter the Review", value = '', style = {'height': '150px'}),
                     html.Div([html.H1(children='Select an existing review', id='dropdown_h2',style={'padding':5})],style={'backgroundColor':'#d6758d','height': 60}),
                           html.Br(),html.Br(),
                    dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:100] + "...", 'value': i} for i in scrappedReviews.reviews],
                    value = scrappedReviews.reviews[0],
                    style = {'margin-bottom': '30px','backgroundColor':'#af969c'}
                    
                )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px','backgroundColor':'#af969c'}
                        ),
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'}),
                    html.Div(id = 'result'),
                    html.Div(id = 'result1')
                    ],
                       
                className = 'text-center'
                ),
        className = 'mt-4'
        )
    
    return main_layout

@app.callback(
    Output('wordc','children'),
    [
        Input('allbt','n_clicks_timestamp'),
        Input('posbt','n_clicks_timestamp'),
        Input('negbt','n_clicks_timestamp'),
    ]
)
def wordcloudbutton(allbt,posbt,negbt):

    if int(allbt) > int(posbt) and int(allbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('Neucloud.png'))])
    elif int(posbt) > int(allbt) and int(posbt)>int(negbt):
        return html.Div([
            html.Img(src=app.get_asset_url('Poscloud.png'))
            ])
    elif int(negbt) > int(allbt) and int(negbt) > int(posbt):
       return html.Div([
           html.Img(src=app.get_asset_url('Negcloud.png'))
           ])
    else:
        pass
@app.callback(
    Output('result', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
    State('textarea', 'value')
    ]
    )    
def update_app_ui(n_clicks, textarea):
    result_list = check_review(textarea)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Ughhh!! Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Yayyy!!Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")

@app.callback(
    Output('result1', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
     State('dropdown', 'value')
     ]
    )
def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Ughhh!! Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Yayyy!!Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")
    
def main():
    global app
    global project_name
    load_model()
    open_browser()
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    app = None
    project_name = None
if __name__ == '__main__':
    main()