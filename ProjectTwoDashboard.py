#!/usr/bin/env python
# coding: utf-8

# In[22]:


# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from CRUD import CRUD

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "12345"

breed_options = [{'label': animal_type, 'value': animal_type} for animal_type in df['animal_type'].unique()]

breed_counts = df['animal_type'].value_counts()

# Connect to database via CRUD Module
db = CRUD(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'], inplace=True)

## Debug
if isinstance(df, pd.DataFrame) and not df.empty:
    # df is properly defined and not empty
    print(len(df.to_dict(orient='records')))
    print(df.columns)
else:
    # df is either not properly defined or empty
    print("DataFrame is either not properly defined or empty.")

#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


fig = px.pie(values=breed_counts, names=breed_counts.index, title='Species Distribution')
#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.Center(html.B(html.H1('By: Tyler S.'))),
    html.Hr(),
    html.H1(children='Species Distribution'),
    dcc.Graph(id='breed-pie-chart',figure=fig),
    html.Div([
        #FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.

        dcc.Dropdown(
            id='filters',
            options=[{"label": "Domestic Shorthair Mix", "value": "Domestic Shorthair Mix"},
    {"label": "Chihuahua Shorthair Mix", "value": "Chihuahua Shorthair Mix"},
    {"label": "Siamese Mix", "value": "Siamese Mix"},
    {"label": "Labrador Retriever Mix", "value": "Labrador Retriever Mix"},
    {"label": "Cardigan Welsh Corgi Mix", "value": "Cardigan Welsh Corgi Mix"},
    {"label": "Pit Bull Mix", "value": "Pit Bull Mix"},
    {"label": "Labrador Retriever/Australian Cattle Dog", "value": "Labrador Retriever/Australian Cattle Dog"},
    {"label": "Dachshund Wirehair Mix", "value": "Dachshund Wirehair Mix"},
    {"label": "Siamese Mix", "value": "Siamese Mix"},
    {"label": "Boxer/Bullmastiff", "value": "Boxer/Bullmastiff"},
    {"label": "Miniature Schnauzer Mix", "value": "Miniature Schnauzer Mix"},
    {"label": "Pit Bull Mix", "value": "Pit Bull Mix"},
    {"label": "Labrador Retriever Mix", "value": "Labrador Retriever Mix"},
    {"label": "Dachshund/Chihuahua Shorthair", "value": "Dachshund/Chihuahua Shorthair"},
    {"label": "Maltese Mix", "value": "Maltese Mix"},
    {"label": "Domestic Medium Hair Mix", "value": "Domestic Medium Hair Mix"},
    {"label": "Labrador Retriever Mix", "value": "Labrador Retriever Mix"},
    {"label": "Dachshund Mix", "value": "Dachshund Mix"},
    {"label": "Pug/Chihuahua Shorthair", "value": "Pug/Chihuahua Shorthair"},
    {"label": "Miniature Poodle Mix", "value": "Miniature Poodle Mix"},
    {"label": "Miniature Poodle", "value": "Miniature Poodle"},
    {"label": "Dachshund Mix", "value": "Dachshund Mix"},
    {"label": "Border Collie/Queensland Heeler", "value": "Border Collie/Queensland Heeler"},
    {"label": "Australian Cattle Dog Mix", "value": "Australian Cattle Dog Mix"},
    {"label": "Chihuahua Shorthair Mix", "value": "Chihuahua Shorthair Mix"},
    {"label": "Domestic Medium Hair Mix", "value": "Domestic Medium Hair Mix"},
    {"label": "Domestic Shorthair Mix", "value": "Domestic Shorthair Mix"},
    {"label": "Yorkshire Terrier Mix", "value": "Yorkshire Terrier Mix"},
    {"label": "Chinese Crested Mix", "value": "Chinese Crested Mix"},
    {"label": "Chihuahua Shorthair Mix", "value": "Chihuahua Shorthair Mix"},
    {"label": "Beagle Mix", "value": "Beagle Mix"},
    {"label": "Labrador Retriever Mix", "value": "Labrador Retriever Mix"}],
            multi=True,  # Allow multiple selections
            placeholder='Select Breeds...'
        )
    ]),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here 
                         page_action='native',
                         page_size=10,
                         filter_action='native',
                         sort_action='native',
                         sort_mode='multi',
                         row_selectable='multi',
                         selected_rows=[],
                        ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
        ),
        html.Div(
            id='map-id',
            className='col s12 m6',
        )
    ])
])

#############################################
# Interaction Between Components / Controller
#############################################



@app.callback(Output('datatable-id','data'),
              [Input('filters', 'value')])
def update_dashboard(selected_species):
    if not selected_species:
        # If no species are breeds, return the original data
        return df.to_dict('records')
    else:
        # Construct a MongoDB query to filter by selected reeds
        query = {"breed": {"$in": selected_species}}
        filtered_data = db.read(query)
        filtered_df = pd.DataFrame.from_records(filtered_data)
        if '_id' in filtered_df.columns:
            filtered_df.drop(columns=['_id'], inplace=True)
        return filtered_df.to_dict('records')
    
    # Return the filtered data in the appropriate format
    return filtered_df.to_dict('records')

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
    if viewData is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else: 
        row = index[0]
        
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]



app.run_server(debug=True)


# In[ ]:





# In[ ]:




