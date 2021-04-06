import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from dash.dependencies import Output, Input, State
import dash_table
import numpy as np
from flask import Flask, send_from_directory
from urllib.parse import quote as urlquote
import gspread
from oauth2client.service_account import ServiceAccountCredentials




drive=pd.read_csv('drivedata.csv')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
application = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
df = pd.read_csv('data.csv')
df.Date=pd.to_datetime(df.Date,format="%d-%m-%Y") 
import_file = pd.read_csv('import_file.csv')
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()

app.layout = dbc.Container(style={'backgroundColor': colors['background'],'width':'1200px'},children = [
    html.H1(
        children='Import Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='For Reordering and Import SKU Tracking', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.H4(children='Vendor Performance Quantity and Sale',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop':'30px',
        }
    ),
    html.H5(children='Select the Date Range',
        style={
            'textAlign': 'left',
            'color': colors['text'],
            'paddingLeft':'10px',
        }
    ),
    html.Div(
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=dt(2023, 9, 19),
            initial_visible_month=dt(2019, 12, 1),
            end_date=dt.now(),
            start_date = start,
            style={
                'width': '100%',
                'padding': '10px',


            }
        ),

    ),
    html.Div(
	    dcc.Dropdown(
	        id='dropdown_vendor',
	        options=[
	            {'label': i, 'value': i} for i in df.Vendor.unique()
	        ],
            value="Aaina Art N Craft",
	        className='mt-4',
	    ),style={'width': '50%','padding': '10px'}

    ),
	dbc.Row([
        dbc.Col([
            html.H4(children='Quantity WISE',
		        style={
		            'textAlign': 'center',
		            'color': colors['text']
		        }
	    	),
            dcc.Graph(id="import data"),
        ], className="six columns"),
        dbc.Col([
            html.H4(children='Sale Wise',
		        style={
		            'textAlign': 'center',
		            'color': colors['text']
		        }
	    	),
            dcc.Graph(id="import data Line Total"),
        ], className="six columns")

    ], className="row"),
    dbc.Row([
        dbc.Col([
	         dbc.Card(
	                dbc.CardBody([
	                    html.H4("Controls", className="card-title"),
	                    dcc.Dropdown(
	                    id='dropdown',
	                    options=[
	                        {'label': i, 'value': i} for i in df['Normal SKU'].unique()
	                    ],

	                    multi=True,
	                    value=['UPT-37910'],
	                    # className='m-4',

	                    ),
	                ]),color="warning",
	            )  
        	], className="six columns"),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(id='table_sku'),
                color="dark", inverse=True,
                className='mt-4',


            )
        ],className="six columns"),
      dbc.Col([
            dcc.Graph(id="import_data_line_tot"),
        ],style={'padding':'30px'}, width=12)

    ],style={'paddingTop':'30px'}, className="row"),

    html.H4("SKU Wise Channel Performance",
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'paddingTop':'30px',
        }


    ),

    dash_table.DataTable(id='sku_channel_wise_perf',
        # columns=[{"name": i, "id": i} for i in df.columns],
        style_header={'backgroundColor': 'rgb(30, 30, 30)','color':'white'},
        style_cell={
            'backgroundColor': 'white',
            'color': 'rgb(50, 50, 50)',
            # 'overflow': 'hidden',
            # 'textOverflow': 'ellipsis',
            'minWidth': '128px', 'width': '128px', 'maxWidth': '128px',
            'textAlign':'center',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
        },
        # style_table={'overflowY': 'scroll'},
        fixed_rows={'headers': True},
        page_action="native",
        page_current=0,
        sort_action="native",
        sort_mode="multi",
        filter_action='native',
        column_selectable="single",
        selected_columns=[],
        selected_rows=[],
        export_format='xlsx',
        export_headers='display',
        # style_data_conditional=styles
    ),



        
    dbc.Row([
        
        html.Div(
            dbc.Col([
                 dbc.Card(
                        dbc.CardBody([
                            html.H4("Inventory", className="card-title"),
                            dbc.Input(
                                id="inv_number", type="number",
                                debounce=True, placeholder="Inventory Less than",
                            ),

                        ]),color="warning",
                    ),  
            ], className="six columns"),

            ),
    ] ,style={'padding':'10px'}, className="row"),
    html.Div([

        dbc.Button('Refresh', id='fetch_data', n_clicks=0),
        dash_table.DataTable(id='drive_table',
            style_header={'backgroundColor': 'rgb(30, 30, 30)','color':'white'},
            style_cell={
                'backgroundColor': 'white',
                'color': 'rgb(50, 50, 50)',
                # 'overflow': 'hidden',
                # 'textOverflow': 'ellipsis',
                'minWidth': '128px', 'width': '128px', 'maxWidth': '128px',
                'textAlign':'center',
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
            },
            style_table={'overflowY': 'scroll'},
            fixed_rows={'headers': True},
            page_action="native",
            page_current=0,
            sort_action="native",
            sort_mode="multi",
            filter_action='native',
            column_selectable="single",
            selected_columns=[],
            selected_rows=[],
            export_format='xlsx',
            export_headers='display',
            style_data_conditional=[

                {

                
                    'if': {
                        'filter_query': '{INV} < 30',
                        'column_id': 'INV'
                    },
                    'backgroundColor': 'rgb(255, 128, 0)',
                    'color': 'white'
                },
                {

                
                    'if': {
                        'filter_query': '{INV} < 1',
                        'column_id': 'INV'
                    },
                    'backgroundColor': 'rgb(255, 0, 0)',
                    'color': 'white'
                }

            ],
        ),

    ])
])
##app layout Ends Here#####
##################################################FOR API FETCHING#########################################################################################
@app.callback(
    [Output("drive_table", "data"),Output("drive_table", "columns")],
    [Input("fetch_data", "n_clicks"),Input('inv_number', 'value')],
)
def update_drive_graph(n_clicks,inv_number):

    if((n_clicks>0) | (inv_number is not None)):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        gc = gspread.service_account(filename='forreordering-38e3f0bc72c3.json')

        wks = gc.open("RE-ORDER Sheet").sheet1
        data = wks.get_all_values()
        headers = data.pop(0)
        drive = pd.DataFrame(data, columns=headers)

        inv_doc = gc.open("Benzara Pico Inventory Maintainace").sheet1
        inv_data =inv_doc.get_all_values() 
        inv_headers = inv_data.pop(0)
        inv_drive = pd.DataFrame(inv_data, columns=inv_headers)
        # print("Print Live Inv")
        # print(inv_drive.head())
        # drive = drive[['SKU', 'Masked SKU',  'Vendor' , 'Category', 'Production',  'Intransit' ,  'Proposed Quantity','30Days' , '90Days' , '180Days' ,'360Days','INV']]
        # print(drive.dtypes)
        # print(drive.head())
        # drive['INV'] = drive['INV'].astype(str).astype(int)
        # print(drive.dtypes)

        # if(inv_number is not None):
            # drive = drive[drive['INV']< inv_number]
        # print(drive)
        return drive.to_dict('records'),[{"name": 'SKU', "id": 'SKU'}, 
            {"name": 'Masked SKU', "id": 'Masked SKU'},
            {
                    'id': 'image',
                    'name': 'image',
                    'presentation': 'markdown',
                    # 'height':'10%', 'width':'10%',
                },
            {"name": 'Vendor', "id": 'Vendor'},
            {"name": 'Category', "id": 'Category'},
            {"name": 'INV', "id": 'INV'},
            {"name": 'INITIAL ORDER', "id": 'INITIAL ORDER'},
            {"name": 'LIVE DATE', "id": 'LIVE DATE'},
            {"name": 'Production', "id": 'Production'},
            {"name": 'Intransit', "id": 'Intransit'},
            {"name": 'Proposed Qty/MOnth', "id": 'Proposed Qty/MOnth'},
            {"name": '30Days', "id": '30Days'},
            {"name": '90Days', "id": '90Days'},
            {"name": '180Days', "id": '180Days'},
            {"name": '360Days', "id": '360Days'},
            {"name": 'Out of Stock Status', "id": 'Out of Stock Status'},
            {"name": 'COMMENTS', "id": 'COMMENTS'},


            ]
    else:
        drive=pd.read_csv('drivedata.csv')
        # print(drive)

        return drive.to_dict('records'),[{"name": 'SKU', "id": 'SKU'}, 
            {"name": 'Masked SKU', "id": 'Masked SKU'},
            {
                    'id': 'image',
                    'name': 'image',
                    'presentation': 'markdown',
                    # 'height':'10%', 'width':'10%',
                },
            {"name": 'Vendor', "id": 'Vendor'},
            {"name": 'Category', "id": 'Category'},
            {"name": 'INV', "id": 'INV'},
            {"name": 'INITIAL ORDER', "id": 'INITIAL ORDER'},
            {"name": 'LIVE DATE', "id": 'LIVE DATE'},
            {"name": 'Production', "id": 'Production'},
            {"name": 'Intransit', "id": 'Intransit'},
            {"name": 'Proposed Qty/MOnth', "id": 'Proposed Qty/MOnth'},
            {"name": '30Days', "id": '30Days'},
            {"name": '90Days', "id": '90Days'},
            {"name": '180Days', "id": '180Days'},
            {"name": '360Days', "id": '360Days'},
            {"name": 'Out of Stock Status', "id": 'Out of Stock Status'},
            {"name": 'COMMENTS', "id": 'COMMENTS'},




            ]




#######################################for sku performence############################################

@app.callback(
    [Output("sku_channel_wise_perf", "data"),Output("sku_channel_wise_perf", "columns")],
    [Input(component_id = 'dropdown', component_property='value'),
     Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
     Input(component_id = 'my-date-picker-range', component_property = 'end_date'),],
    )
def update_monthly_sales1(input_value,start_date,end_date):

    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = datetime.datetime(2019, 10, 1)

    if end_date is not None:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime(datetime.datetime.now())
    df = pd.read_csv('data.csv')
    df.Date=pd.to_datetime(df.Date,format="%d-%m-%Y") 

    normal_sku = []
    Line_tot = []
    quantity = []
    lol = pd.DataFrame(columns=['Normal SKU','Month','Sales Channel','Line Total','Quantity'])

    for i in input_value:
        dff = df[(df['Normal SKU'] == i) & ((df.Date >= start_date) & (df.Date <= end_date))]
        normal_sku.append(dff['Normal SKU'].unique())
        temp = float("{0:.2f}".format(dff['Line Total'].sum()))
        temp1 = float("{0:.2f}".format(dff['Quantity'].sum()))
        Line_tot.append(temp)
        quantity.append(temp1)
        meow = dff.groupby(['Normal SKU','Month','Sales Channel'])["Line Total", "Quantity"].apply(lambda x : x.astype(int).sum()).reset_index()
        lol = lol.append(meow)

    convert_dict = {'Quantity': int,
                    'Line Total': float,
                    'Month': int,
                    }
    d = pd.DataFrame({
        'Normal SKu':normal_sku,
        'Line Total':Line_tot,
        'Quantity':quantity
    })

    # table =  dbc.Table.from_dataframe(d, striped=True,style={'color':'white'})
    # data1 = lol.to_dict('records')
    # cols = [{"name": i, "id": i} for i in lol.columns]
    test = pd.pivot_table(lol, values='Quantity', index=['Normal SKU'],
                    columns=['Sales Channel'], aggfunc=np.sum)
    flattened = pd.DataFrame(test.to_records())
    # print('flattened',flattened)
    return flattened.to_dict('records'),[{"name": i, "id": i} for i in flattened.columns]

######################################For Dropdown####################################################################################
@app.callback(
    [Output(component_id = 'dropdown', component_property='options'),
         Output(component_id = 'dropdown', component_property='value')],
    [Input(component_id = 'dropdown_vendor', component_property='value'),
    Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
     Input(component_id = 'my-date-picker-range', component_property = 'end_date')],
    )
def update_dropdown_vendor(input_value,start_date,end_date):
    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = datetime.datetime(2019, 10, 1)

    if end_date is not None:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime(datetime.datetime.now())

    if input_value is not None:
        test = df[(df['Vendor']==input_value) & ((df.Date >= start_date) & (df.Date <= end_date))]
        vals = list(test['Normal SKU'].unique())
        return [ {'label': i, 'value': i} for i in vals],vals[:5]

###################################for the table#########################################################################################
@app.callback(
    Output(component_id = 'table_sku', component_property='children'),
    [Input(component_id = 'dropdown', component_property='value'),
     Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
     Input(component_id = 'my-date-picker-range', component_property = 'end_date'),],
    )
# def update_monthly_sales(input_value,month,start_date,end_date):
def update_monthly_sales(input_value,start_date,end_date):

    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = datetime.datetime(2019, 10, 1)

    if end_date is not None:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime(datetime.datetime.now())
    df = pd.read_csv('data.csv')
    df.Date=pd.to_datetime(df.Date,format="%d-%m-%Y") 

    normal_sku = []
    Line_tot = []
    quantity = []
    lol = pd.DataFrame(columns=['Normal SKU','Month','Sales Channel','Line Total','Quantity'])

    for i in input_value:
        dff = df[(df['Normal SKU'] == i) & ((df.Date >= start_date) & (df.Date <= end_date))]
        normal_sku.append(dff['Normal SKU'].unique())
        temp = float("{0:.2f}".format(dff['Line Total'].sum()))
        temp1 = float("{0:.2f}".format(dff['Quantity'].sum()))
        Line_tot.append(temp)
        quantity.append(temp1)
        meow = dff.groupby(['Normal SKU','Month','Sales Channel'])["Line Total", "Quantity"].apply(lambda x : x.astype(int).sum()).reset_index()
        lol = lol.append(meow)

    convert_dict = {'Quantity': int,
                    'Line Total': float,
                    'Month': int,
                    }
    d = pd.DataFrame({
        'Normal SKu':normal_sku,
        'Line Total':Line_tot,
        'Quantity':quantity
    })

    table =  dbc.Table.from_dataframe(d, striped=True,style={'color':'white'})
    data1 = lol.to_dict('records')
    cols = [{"name": i, "id": i} for i in lol.columns]
    return (table)
## FOr the Miltiple line graphs SKUs###############################################################################
@app.callback(
    Output(component_id = 'import_data_line_tot', component_property='figure'),
    [Input(component_id = 'dropdown', component_property='value'),
     # Input(component_id = 'month-range', component_property='value'),
     Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
     Input(component_id = 'my-date-picker-range', component_property = 'end_date'),],
    )
# def update_fig1(input_value,month,start_date,end_date):
def update_fig1(input_value,start_date,end_date):


    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = datetime.datetime(2019, 10, 1)

    if end_date is not None:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime(datetime.datetime.now())
    df = pd.read_csv('data.csv')
    df.Date=pd.to_datetime(df.Date,format="%d-%m-%Y") 
    # df.Date=df.Date.astype('datetime64[ns]')

    data=[]
    for i in input_value:
        dff = df[(df['Normal SKU'] == i) & ((df.Date >= start_date) & (df.Date <= end_date))]
        # dff = dff[(dff["Month"] >= month[0]) & (dff["Month"] <= month[1])]
        dff = dff.sort_values(by='Date')
        # for plotting different variables we will be using different function
        trace_line_tot = go.Scatter(x=dff.Date,
                                y=dff['Line Total'],
                                name=i,
                                mode = 'lines',marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}},
                                )
        data.append(trace_line_tot)


    return{
        "data": data,
        "layout":go.Layout(title="Line Total Wise Sales", colorway=['#C70039', '#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Line Total(in dollars)"}, xaxis={"title": "Date"},  )
    }

###############################IMPORT DATA#################################################################
@app.callback(
    Output(component_id = 'import data', component_property='figure'),
    [Input(component_id = 'dropdown_vendor', component_property='value'),
     Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
     Input(component_id = 'my-date-picker-range', component_property = 'end_date')],
    )
def update_fig(input_value,start_date,end_date):
    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = datetime.datetime(2019, 10, 1)

    if end_date is not None:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime(datetime.datetime.now())

    df1 = pd.read_csv('data.csv')
    df1.Date=pd.to_datetime(df1.Date,format="%d-%m-%Y")
    df1.Quantity = df1.Quantity.astype(int)

    df1 = df1[(df1['Vendor'] == input_value) & ((df1.Date >= start_date) & (df1.Date <= end_date))]
    df1 = df1.set_index(['Vendor']) 
    df2 = df1[['Date','Quantity']]
    df2 = pd.DataFrame(df2.groupby('Date')['Quantity'].agg(['sum']))
    df2 = df2.reset_index()
    data = []

    # for plotting different variables we will be using different function
    trace_line_tot = go.Scatter(x=pd.Series(df2['Date']),
                                y=df2['sum'],
                                name=input_value,
                                line=dict(color='#f44242'))
    data.append(trace_line_tot)
    layout = {"title": input_value}
    return{
        "data":data,
        "layout" :layout
    }
############################################import data Line Total###########################################################################
@app.callback(
    Output(component_id = 'import data Line Total', component_property='figure'),
    [Input(component_id = 'dropdown_vendor', component_property='value'),
     Input(component_id = 'my-date-picker-range', component_property = 'start_date'),
     Input(component_id = 'my-date-picker-range', component_property = 'end_date')],
    )
def update_fig(input_value,start_date,end_date):
    if start_date is not None:
        start_date = pd.to_datetime(start_date)
    else:
        start_date = datetime.datetime(2019, 10, 1)

    if end_date is not None:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime(datetime.datetime.now())

    df1 = pd.read_csv('data.csv')
    df1.Date=pd.to_datetime(df1.Date,format="%d-%m-%Y") 
    # df1.Date = df1.Date.astype('datetime64[ns]')
    df1 = df1[(df1['Vendor'] == input_value) & ((df1.Date >= start_date) & (df1.Date <= end_date))]
    df1 = df1.set_index(['Vendor']) 
    df2 = df1[['Date','Line Total']]
    df2['Line Total'] = df2['Line Total'].astype(np.float16)
    df2 = pd.DataFrame(df2.groupby('Date')['Line Total'].agg(['sum']))
    df2 = df2.reset_index()
    data = []
    # print(df2)

    # for plotting different variables we will be using different function
    trace_line_tot = go.Scatter(x=pd.Series(df2['Date']),
                                y=df2['sum'],
                                name=input_value,
                                line=dict(color='#f44242'))
    data.append(trace_line_tot)
    layout = {"title": input_value}
    return{
        "data":data,
        "layout" :layout
    }
if __name__ == '__main__':
    application.run(debug=True, port=8080,host='0.0.0.0')
