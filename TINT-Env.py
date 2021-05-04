#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import panel as pn
pn.extension('plotly')
import pandas as pd
import plotly.io as pio
pio.renderers.default='iframe'
# import locale

# locale.setlocale(locale.LC_ALL, 'th_TH')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

envi_df = pd.read_excel("D:/Onedrive(work)\OneDrive - Thailand Institute of Nuclear Technology(Public Organizaion)/Documents/Management/แผนปฏิบัติงาน/2564/(ทีม4)ส่วนงานสิ่งแวดล้อม/Data collection 2020 V3 edit GPS 02-03-64(corrected).xlsx", sheet_name="ข้อมูลสิ่งแวดล้อม 2563", usecols="A:I")
GPS_df = pd.read_excel("D:/Onedrive(work)\OneDrive - Thailand Institute of Nuclear Technology(Public Organizaion)/Documents/Management/แผนปฏิบัติงาน/2564/(ทีม4)ส่วนงานสิ่งแวดล้อม/Data collection 2020 V3 edit GPS 02-03-64(corrected).xlsx", sheet_name="ข้อมูลสิ่งแวดล้อม 2563", usecols="M:P",index_col=[0,1])
envi_df=envi_df.drop_duplicates()
GPS_df=GPS_df.drop_duplicates()
# envi_df.head()
# GPS_df.head()
result = envi_df.join(GPS_df,on=['Place','Site'], how='inner')


# In[34]:


import plotly.express as px

token = open(".mapbox_token").read()
place_map = px.scatter_mapbox(result, lat="Latitude", lon="Longitude", hover_name="Place", hover_data=["Site","ชนิดตัวอย่าง","สิ่งตรวจวัด","หน่วย"],
                        color_continuous_scale=px.colors.sequential.Agsunset, zoom=8, color='ค่านับวัด',size='ค่านับวัด', title="แผนที่จุดเก็บตัวอย่าง")
place_map.update_layout(mapbox_style="open-street-map", mapbox_accesstoken=token)
place_map.update_layout(margin={"r":0,"t":35,"l":0,"b":0},paper_bgcolor="white",font={"color":"black"})


# In[35]:




def check(site,sample):
    df = result.set_index(['Site', 'ชนิดตัวอย่าง'])
    for i in df.index.unique().tolist():
        if i[0] == site:
            if i[1]==sample and i[0]==site :
                return True
    return False


# In[41]:


import plotly
import plotly.graph_objects as go 
# import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets=[{'crossorigin':'anonymous','rel':'stylesheet','href':"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"}]

app = JupyterDash(__name__,external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)
server = app.server
site_indicators = result['Site'].unique().tolist()
all_options={}
config={"editable":True, "edits":{"shapePosition": False}, #"scrollZoom": False,
    'modeBarButtonsToAdd':['drawline',
#                                         'drawopenpath',
#                                         'drawclosedpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ],
       'modeBarButtonsToRemove':['lasso2d',
#                                         'drawopenpath',
#                                         'drawclosedpath',
                                        'zoomIn2d',
                                        'zoomOut2d',
                                       ]}
for i in site_indicators:
    all_options[i]=result['ชนิดตัวอย่าง'][result['Site']==i].unique()
app.layout = html.Div( children=[
    html.Div(className="w3-bar w3-top  w3-large w3-amber", style={"z-index":4}, children=[
       html.Button(" Menu", id="open-menu-button", n_clicks=0, className=
                "w3-bar-item w3-button w3-hide-large w3-hover-none w3-hover-text-light-grey fa fa-bars"),
        html.Span(' กัมมันตภาพรังสีในสิ่งแวดล้อมรอบ สทน. ทั้ง 3 แห่ง', className='w3-bar-item w3-right fa fa-dashboard fa-lg')]
    ),  
    html.Nav(id="mySidebar", className="w3-mobile w3-sidebar w3-collapse w3-sand w3-animate-left", style={"z-index":4, "width":"200px"}, children=[
#         html.Button("Close &times", id="close-menu-button", n_clicks=0, className="w3-bar-item w3-button w3-large w3-hide-large"),
        html.Div(className="w3-container", children=[
#             html.I(className="fa fa-institution"),
            html.Span(" สาขา",className="fa fa-institution")
        ]),
        html.Div(className="w3-bar-block", children=[
           html.Div(className="w3-bar-item", children=[ 
                dcc.RadioItems(
                    id='site-radio',
                    options=[{'label': i, 'value': i} for i in all_options.keys()],
                    value='คลองห้า',
                    labelStyle={'display':'block'}
                )
           ]),
           html.Div(className="w3-container", children=[ 
#                html.I(className="fa fa-flask"),
               html.Span(" ชนิดตัวอย่าง",className="fa fa-flask")
           ]),
           html.Div(className='w3-bar-block w3-padding', children=[ 
                dcc.Dropdown(id='sample-dropdown',clearable=False)
           ])
        ])
    ]),  
    html.Div(className="w3-main",style={'margin-left':200, 'margin-top':43}, children=[
        html.Div(className="w3-row-padding  w3-margin-bottom", children=[
            html.Div(className="w3-half", children=[
                html.Div(className="w3-container w3-card w3-animate-top w3-padding-16", children=[
                    dcc.Graph(config=config,id='fig_1')
                ])
            ]),        
            html.Div(className="w3-half", children=[
                html.Div(className="w3-container w3-card w3-animate-top  w3-padding-16", children=[
                    dcc.Graph(config=config,id='fig_2')
                ])
            ])
        ]),
        html.Div(className="w3-card w3-animate-right w3-margin-top w3-margin-bottom w3-padding-small",children=[dcc.Graph(figure=place_map)]),
        html.Div(
            html.Span(className="w3-bar-item  w3-text-grey w3-light-grey w3-right", children=
                "สำรวจและจัดทำโดย: ฝ่ายความปลอดภัยด้านนิวเคลียร์ สถาบันเทคโนโลยีนิวเคลียร์แห่งชาติ (องค์การมหาชน)"),
            className="w3-bar w3-panel w3-bottom"
        )    
        
    ])
    
])        
    
@app.callback(
    Output('mySidebar','style'),
    Input('open-menu-button', 'n_clicks')
)
def update_style(n_clicks):
    if n_clicks%2 == 1:
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(
    Output('sample-dropdown', 'options'),
    Input('site-radio', 'value')
)
def set_sample_options(selected_site):
    return [{'label': i, 'value': i} for i in all_options[selected_site]]

@app.callback(
    Output('sample-dropdown', 'value'),
    Input('sample-dropdown', 'options')
)
def set_sample_value(available_options):
    return available_options[0]['value']

@app.callback(
    [Output('fig_1', 'figure'),
    Output('fig_2', 'figure')],
    [Input('site-radio', 'value'),
    Input('sample-dropdown', 'value')]
)
def update_figure(site_radio_name, sample_dropdown_name):    
        layout=go.Layout(
                hoverlabel=dict(
#                     bgcolor='white', #'rgba(200,200,200,1)',
                    font_size=14,
#                     font_color='black', #'rgba(150,255,255,1)',       
                ), #plot_bgcolor='rgba(253,245,230,1)', 
                    yaxis=dict(showgrid=False),
                modebar=dict(orientation="v")
            )
        fig1=go.Figure(layout=layout)
        fig2=go.Figure(layout=layout)
        for i in result['สิ่งตรวจวัด'][result['ชนิดตัวอย่าง']==sample_dropdown_name].unique(): 
            a=result['หน่วย'][(result['Site']==site_radio_name) & (result['สิ่งตรวจวัด']==i) &                                                            (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0)].tolist()
            b=result['วันที่เก็บตัวอย่าง'][(result['Site']==site_radio_name) & (result['สิ่งตรวจวัด']==i) &                                                            (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0)].dt.strftime("%d %b %Y").tolist()
            xx=result['สิ่งตรวจวัด'][(result['Site']==site_radio_name) & (result['สิ่งตรวจวัด']==i) &                                                             (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0)]
            yy=result['ค่านับวัด'][(result['Site']==site_radio_name) & (result['สิ่งตรวจวัด']==i) &                                                            (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0)]
            zz=result['อัตราปริมาณรังสีต่อปี'][(result['Site']==site_radio_name) & (result['สิ่งตรวจวัด']==i) &                                                            (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0)]
            fig1.add_trace(go.Violin( x=xx,
                                    y=yy, 
                           name=i, #scalegroup="สิ่งตรวจวัด", 
                           marker=dict(size=6, line=dict(width=0.5, color='black',outliercolor='white')), 
                           box_visible=True, meanline_visible=True,meanline_color='white',
                           box_fillcolor='grey',box_line_color='black',line_width=1,points='all',jitter=0.5, 
                           marker_symbol="diamond", marker_line_color='black',
                           text = result['Place'][(result['สิ่งตรวจวัด']==i) & (result['Site']==site_radio_name) & (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0) ].tolist(),
                           customdata =np.stack((a,b),axis=1) , 
                           hovertemplate="<b>%{text}</b><br><b>spec.activity: \
</b>%{y} %{customdata[0]}<br><b>วันที่เก็บตัวอย่าง:</b> %{customdata[1]}"))
            fig1.add_annotation(dict(text="Drag me to where you want.<br>Then edit me as you like.", 
                               clicktoshow="onoff", visible=False,
                              x=i, y=yy.min(), arrowhead=3, arrowcolor='cyan'))
            aa =["uSv/y" for c in a]
            fig2.add_trace(go.Violin( x=xx,
                                    y=zz, 
                           name=i, #scalegroup="สิ่งตรวจวัด", 
                           marker=dict(size=6, line=dict(width=0.5, color='black',outliercolor='white')), 
                           box_visible=True, meanline_visible=True,meanline_color='white',
                           box_fillcolor='grey',box_line_color='black',line_width=1,points='all',jitter=0.5, 
                           marker_symbol="diamond", marker_line_color='black',
                           text = result['Place'][(result['สิ่งตรวจวัด']==i) & (result['Site']==site_radio_name) & (result['ชนิดตัวอย่าง']==sample_dropdown_name) & (result['ค่านับวัด']>0) ].tolist(),
                           customdata =np.stack((aa,b),axis=-1) ,
                           hovertemplate="<b>%{text}</b><br><b>spec.activity: \
</b>%{y} %{customdata[0]}<br><b>วันที่เก็บตัวอย่าง:</b> %{customdata[1]}"))
            fig2.add_annotation(dict(text="Drag me to where you want.<br>Then edit me as you like.", 
                               clicktoshow="onoff", visible=False,
                              x=i, y=zz.min(), arrowhead=3, arrowcolor='cyan'))
        fig1.update_layout(
            title=sample_dropdown_name+site_radio_name + " > Specific Activity",
            margin=dict(l=0, r=50, t=30, b=50),
            font=dict(
                family="Rockwell Nova",
                color="black"
               # size=14
            ),
            hoverdistance=10,
            yaxis=dict(title='ค่านับวัด',zeroline=False), #, type="log"),
            xaxis=dict(title='สิ่งตรวจวัด'),
            legend=dict(
                x=0.9,
                borderwidth=1,
#                 bordercolor="darkcyan",
#                 bgcolor="darkslateblue",
                itemclick='toggleothers'           
            ),
#             paper_bgcolor="darkslategrey",
            dragmode='drawline',
                  # style of new shapes
            newshape=dict(line_color='red',
                                fillcolor='grey',
                                opacity=0.2,
                                #layer="below",
                                line_width=2)
        )
        fig2.update_layout(
            title=sample_dropdown_name+site_radio_name + " > Committed Effective Dose",
            margin=dict(l=0, r=50, t=30, b=50),
            font=dict(
                family="Rockwell Nova",
                color="black"
               # size=14
            ),
            
            yaxis=dict(title='อัตราปริมาณรังสีต่อปี',zeroline=False), #, type="log"),
            xaxis=dict(title='สิ่งตรวจวัด'),
            legend=dict(
                x=0.9,
                borderwidth=1,
#                 bordercolor="darkcyan",
#                 bgcolor="darkslateblue",
                itemclick='toggleothers'           
            ),
#             paper_bgcolor="darkslategrey",
            dragmode='drawline',
                  # style of new shapes
            newshape=dict(line_color='red',
                                fillcolor='grey',
                                opacity=0.2,
                                #layer="below",
                                line_width=2)
        )    
        return [fig1, fig2]
if __name__ == '__main__':
app.run_server(debug=True)

