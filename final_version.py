# data manipulation
import pandas as pd

# plotly 
import plotly.express as px
import plotly.graph_objs as go

# dashboards
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

import numpy as np

df=pd.read_csv('video_games_sales.csv')
vgsales=pd.read_csv('video_games_sales.csv')
game = pd.read_csv('video_games_sales.csv',parse_dates=['Year'], encoding='unicode_escape')
game20 = game.loc[game['Region']=='Global_Sales'].sort_values('Sales',ascending=False).head(20).sort_values('Sales',ascending=True)
df4 = game.loc[game['Region']=='Global_Sales'].sort_values('Sales',ascending=False).\
    head(20).sort_values('Sales',ascending=True)
df_remarks = pd.read_csv('df4.csv')

dfpage=pd.DataFrame(
    data=[['Platform','PS2, X360, PS3'],['Year','1980-2016'],['Genre','Action, Sports, Shooter'],['Publisher','Nintendo, EA, Activision'],['Region','Global, NA, EU, JP, Other']],
    columns=['Column','Example'])
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

template = {"layout": {"paper_bgcolor": colors['background'], "plot_bgcolor": colors['text']}}

n_selected_indicator = {
        "data": [
            {
                "type": "indicator",
                "value": df.loc[df['Region']=='Global_Sales']['Sales'].sum(),
                "number": {"font": {"color": "#7FDBFF"}},
            }
        ],
        "layout": {
            "template": template,
            "height": 90,
            "margin": {"l": 5, "r": 5, "t": 5, "b": 5},
        },
}

boxdf=df[df['Region']=='Global_Sales'].loc[:,['Name','Sales']].reset_index().drop(columns='index')
fig1 = px.box(data_frame=boxdf, y='Sales', width=400, height=450, hover_name='Name')
fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    title = go.layout.Title(text='Video Game Global Sales Boxplot',font=go.layout.title.Font(size=30)), yaxis_title = 'Global Sales')

region_ysales=df.groupby(['Year','Region']).Sales.sum().unstack()
regions = region_ysales.columns
colors = ['rgb(240,249,232)', 'rgb(186,228,188)', 'rgb(123,204,196)', 'rgb(67,162,202)', 'rgb(8,104,172)']


fig2 = go.Figure()

for region, col in zip(regions, colors):
    
    fig2.add_trace(go.Scatter(name = region,
                             x = region_ysales.index, 
                             y = region_ysales[region],
                             mode = 'lines', 
                             line = dict(color = col),
                             ))

fig2.update_layout(
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    font_color='#7FDBFF',
    title = go.layout.Title(text='Video Game Sales in Different Regions',font=go.layout.title.Font(size=30)),
    xaxis_title = 'Year', 
    yaxis_title = 'Sales')

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#111111',
    'color': '#7FDBFF',
    'padding': '6px'
}

fig1_4 = go.Figure(go.Bar(
            x=df4.Sales,
            y=df4.Name,
            orientation='h'))
fig1_4.update_layout(
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    font_color='#7FDBFF',
    title='Worldwide Top 20 Best Sellers')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(style={'backgroundColor': '#111111'},children=[
    html.H1("Video Games' Sales Dashboard",
            style={'color': '#7FDBFF',
                   'fontSize': '60px'}),
    dcc.Tabs([
        dcc.Tab(label='Data Summary',style=tab_style, selected_style=tab_selected_style,children=[
 html.Div([

        # Top part of page1
        # It has two subdivisions (left and right subdivisions)
        html.Div([
            # top left division: Data Summary & Box
            html.Div([
                html.H1('Data Column Overview', style={'textAlign':'left','color':'#7FDBFF', 'fontSize':'30px'}),
                dash_table.DataTable(
                data=dfpage.to_dict('rows'),
                columns=[{"name": i, "id": i} for i in dfpage.columns],
                style_cell_conditional=[{'textAlign': 'left'}],
                style_data={
                'color': '#7FDBFF',
                'backgroundColor': '#111111'
                },
                style_header={
                'backgroundColor': '#111111',
                'color': '#7FDBFF',
                'fontWeight': 'bold'
                }
                ),
                html.Br(),
                html.P('Total Sales: (M$)',style={'textAlign':'left','color':'#7FDBFF','fontSize':'30px'}),
                dcc.Graph(figure=n_selected_indicator, style={"height": 200})
            ],style={'width': '45%', 'display': 'inline-block'}),

            # top right division: Video Game Global Sales Boxplot
            html.Div([
                dcc.Graph(figure=fig1)        
            ],style={'width': '45%', 'float': 'right','display': 'inline-block'})

        ], style={'padding': '10px 5px'}),

        # Bottom part of page1
        html.Div([
            dcc.Graph(figure=fig2)        
        ],style={'width':'100%','display': 'inline-block'})

        ])
        ]
            ),
        dcc.Tab(label='Platform', style=tab_style, selected_style=tab_selected_style,children=[
            html.Div([
# Headline
    html.H1('Platform Analysis',style={'textAlign':'left','color':'#7FDBFF','fontSize':'60px'}),
    html.P('Filter by Game Genre: ',style={'textAlign':'left','color':'#7FDBFF','fontSize':'30px'})
]),

html.Div([
dcc.Dropdown(
            id='genre_dropdown',
            value='All',
            options=[{'label':genre,'value':genre} for genre in vgsales['Genre'].unique()]),
]),

html.Div([
    html.Div([
        html.P('Total Sales of Platform: (M$)',style={'textAlign':'left','color':'#7FDBFF','fontSize':'30px'}),
        dcc.Dropdown(id='Box2_dropdown',value='PS2',
        options=[{'label':platform,'value':platform} for platform in vgsales['Platform'].unique()]),
        dcc.Graph(id='Box2', style={"height": 200}
        ),
        dcc.Graph(id='figure2_platform'),
    ],style={'width': '45%','float': 'left','display': 'inline-block'}),
    html.Div([
        
         
         dcc.Graph(id='figure1_platform'),
    ],style={'width': '45%','float': 'right','display': 'inline-block'}),

]),




# Bottom part of page2
html.Div([
    dcc.Graph(id='figure3_platform')        
],style={'width':'98%','display': 'inline-block'})
        ]
            ),
        dcc.Tab(label='Publisher', style=tab_style, selected_style=tab_selected_style,children=[
            html.Div([
# Headline
    html.H1('Publisher Analysis',style={'textAlign':'left','color':'#7FDBFF','fontSize':'60px'}),
    html.P('Filter by Game Genre: ',style={'textAlign':'left','color':'#7FDBFF','fontSize':'30px'})
]),

html.Div([
dcc.Dropdown(
            id='genre_dropdown_publisher',
            value='All',
            options=[{'label':genre,'value':genre} for genre in vgsales['Genre'].unique()]),
]),

html.Div([
    html.Div([
        html.P('Total Sales of Publisher: (M$)',style={'textAlign':'left','color':'#7FDBFF','fontSize':'30px'}),
        dcc.Dropdown(id='Box3_dropdown',value='Nintendo',
        options=[{'label':publisher,'value':publisher} for publisher in vgsales['Publisher'].unique()]),
        dcc.Graph(id='Box3', style={"height": 200}
        ),
        dcc.Graph(id='figure5'),
    ],style={'width': '45%','float': 'left','display': 'inline-block'}),
    html.Div([
        
         
         dcc.Graph(id='figure4'),
    ],style={'width': '50%','float': 'right','display': 'inline-block'}),

]),




# Bottom part of page3
html.Div([
    dcc.Graph(id='figure6')        
],style={'width':'98%','display': 'inline-block'})
        ]
            ),
        dcc.Tab(label='Top 20 Video Games',style=tab_style, selected_style=tab_selected_style,children=[
            html.H1('Worldwide Top 20 Best Sellers: Core Competitiveness',style={'textAlign':'left','color':'#7FDBFF','fontSize':'42px'}),
    html.A('Move the mouse to see detail',style={'textAlign':'left','color':'#7FDBFF','fontSize':'15px'}),
    html.Div([
        dcc.Graph(id='fig-top20',figure=fig1_4,hoverData={'points': [{'y': 'Wii Sports','x':'82.74'}]},style={"height": 500})
        ]),
    html.Div(id='table4'),
    html.Div([
        dcc.Graph(id='Sales_of_Game')
    ])
        ])
    ])
])

#figure1
@app.callback(
    Output('figure1_platform', 'figure'),
    Input('genre_dropdown', 'value'))
def update_figure1(genre):
    if genre == 'All':
        filtered_df = vgsales
    else:
        filtered_df = vgsales[vgsales.Genre == genre]
    df=filtered_df.groupby(['Platform','Region'])[['Sales']].sum().reset_index()
    df1=df.loc[df['Region']=='Global_Sales'].sort_values(by='Sales',ascending=False).head(5)
    top_5_platform=filtered_df.loc[filtered_df['Platform'].isin(df1['Platform'].tolist())]
    fig3 = go.Figure()
    top_5_platform_update=top_5_platform.groupby(['Year','Platform','Region'])[['Sales']].sum().reset_index()
    top_5_platform_region=top_5_platform_update.loc[top_5_platform_update['Region']!='Global_Sales']
    df11=top_5_platform_region.groupby(['Platform','Region']).Sales.sum().reset_index()
    fig1 = px.bar(df11, x = 'Sales', y = 'Platform', color = 'Region')
    fig1.update_layout(yaxis = {'categoryorder': 'array', 'categoryarray': df1['Platform'].tolist()})
    fig1.update_layout(
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font_color='#7FDBFF',
        title = go.layout.Title(text="Top 5 Platform's Sales by Region",font=go.layout.title.Font(size=20)))

    return fig1

#figure2
@app.callback(
    Output('figure2_platform', 'figure'),
    Input('genre_dropdown', 'value'))
def update_figure1(genre):
    if genre == 'All':
        filtered_df = vgsales
    else:
        filtered_df = vgsales[vgsales.Genre == genre]
    df=filtered_df.groupby(['Platform','Region'])[['Sales']].sum().reset_index()
    NA_platform=df.loc[df['Region']=='NA_Sales'].sort_values(by='Sales',ascending=False).head(3)
    EU_platform=df.loc[df['Region']=='EU_Sales'].sort_values(by='Sales',ascending=False).head(3)
    JP_platform=df.loc[df['Region']=='JP_Sales'].sort_values(by='Sales',ascending=False).head(3)
    Other_platform=df.loc[df['Region']=='Other_Sales'].sort_values(by='Sales',ascending=False).head(3)
    Global_platform=df.loc[df['Region']=='Global_Sales'].sort_values(by='Sales',ascending=False).head(3)

    fig2 = go.Figure(data=[go.Table(
        columnwidth=[15,22,22,22,22,22],
        header=dict(values=['Rank','NA','EU','JP','Other','Global'],
                    fill_color='#111111',
                    align='left'),
        cells=dict(values=[pd.Series([1,2,3]), NA_platform.Platform, EU_platform.Platform, JP_platform.Platform,Other_platform.Platform,Global_platform.Platform],
                fill_color='#111111',
                align='left'))
    ])
    fig2.update_layout(
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    font_color='#7FDBFF',
    title = go.layout.Title(text="Top 3 Platforms in Each Region",font=go.layout.title.Font(size=20))
)
    return fig2


#figure3
@app.callback(
    Output('figure3_platform', 'figure'),
    Input('genre_dropdown', 'value'))
def update_figure(genre):
    if genre == 'All':
        filtered_df = vgsales
    else:
        filtered_df = vgsales[vgsales.Genre == genre]
    df=filtered_df.groupby(['Platform','Region'])[['Sales']].sum().reset_index()
    df1=df.loc[df['Region']=='Global_Sales'].sort_values(by='Sales',ascending=False).head(5)
    top_5_platform=filtered_df.loc[filtered_df['Platform'].isin(df1['Platform'].tolist())]
    fig3 = go.Figure()
    top_5_platform_update=top_5_platform.groupby(['Year','Platform','Region'])[['Sales']].sum().reset_index()
    #figure 3
    fig3=px.line(top_5_platform_update.loc[top_5_platform_update['Region']=='Global_Sales'],x = 'Year', y='Sales',color='Platform')
    
    fig3.update_layout(
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='#7FDBFF',
            title=go.layout.Title(text="Platform Sales by Year",
                                        font=go.layout.title.Font(size=20)),
            width=1250,
            height=570,
    )

    return fig3

@app.callback(
    Output('figure4', 'figure'),
    Input('genre_dropdown_publisher', 'value'))
def update_figure4(genre):
    if genre == 'All':
        filtered_df = vgsales
    else:
        filtered_df = vgsales[vgsales.Genre == genre]
    df=filtered_df.groupby(['Publisher','Region'])[['Sales']].sum().reset_index()
    df1=df.loc[df['Region']=='Global_Sales'].sort_values(by='Sales',ascending=False).head(5)
    top_5_publisher=filtered_df.loc[filtered_df['Publisher'].isin(df1['Publisher'].tolist())]
    fig4 = go.Figure()
    top_5_publisher_update=top_5_publisher.groupby(['Year','Publisher','Region'])[['Sales']].sum().reset_index()
    top_5_publisher_region=top_5_publisher_update.loc[top_5_publisher_update['Region']!='Global_Sales']
    df11=top_5_publisher_region.groupby(['Publisher','Region']).Sales.sum().reset_index()
    fig4 = px.bar(df11, x = 'Sales', y = 'Publisher', color = 'Region')
    fig4.update_layout(yaxis = {'categoryorder': 'array', 'categoryarray': df1['Publisher'].tolist()})
    fig4.update_layout(
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font_color='#7FDBFF',
        title = go.layout.Title(text="Top 5 Publisher's Sales by Region",font=go.layout.title.Font(size=20)),
        height=700,
        width=630
        )

    return fig4

#figure5
@app.callback(
    Output('figure5', 'figure'),
    Input('genre_dropdown_publisher', 'value'))
def update_figure5(genre):
    if genre == 'All':
        filtered_df = vgsales
    else:
        filtered_df = vgsales[vgsales.Genre == genre]
    df=filtered_df.groupby(['Publisher','Region'])[['Sales']].sum().reset_index()
    NA_publisher=df.loc[df['Region']=='NA_Sales'].sort_values(by='Sales',ascending=False).head(3)
    EU_publisher=df.loc[df['Region']=='EU_Sales'].sort_values(by='Sales',ascending=False).head(3)
    JP_publisher=df.loc[df['Region']=='JP_Sales'].sort_values(by='Sales',ascending=False).head(3)
    Other_publisher=df.loc[df['Region']=='Other_Sales'].sort_values(by='Sales',ascending=False).head(3)
    Global_publisher=df.loc[df['Region']=='Global_Sales'].sort_values(by='Sales',ascending=False).head(3)

    fig5 = go.Figure(data=[go.Table(
        columnwidth=[15,22,22,22,22,22],
        header=dict(values=['Rank','NA','EU','JP','Other','Global'],
                    fill_color='#111111',
                    align='left'),
        cells=dict(values=[pd.Series([1,2,3]), NA_publisher.Publisher, EU_publisher.Publisher, JP_publisher.Publisher,Other_publisher.Publisher,Global_publisher.Publisher],
                fill_color='#111111',
                align='left'))
    ])
    fig5.update_layout(
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    font_color='#7FDBFF',
    title = go.layout.Title(text="Top 3 Publishers in Each Region",font=go.layout.title.Font(size=20))
)
    return fig5


#figure6
@app.callback(
    Output('figure6', 'figure'),
    Input('genre_dropdown_publisher', 'value'))
def update_figure6(genre):
    if genre == 'All':
        filtered_df = vgsales
    else:
        filtered_df = vgsales[vgsales.Genre == genre]
    df=filtered_df.groupby(['Publisher','Region'])[['Sales']].sum().reset_index()
    df1=df.loc[df['Region']=='Global_Sales'].sort_values(by='Sales',ascending=False).head(5)
    top_5_publisher=filtered_df.loc[filtered_df['Publisher'].isin(df1['Publisher'].tolist())]
    fig6 = go.Figure()
    top_5_publisher_update=top_5_publisher.groupby(['Year','Publisher','Region'])[['Sales']].sum().reset_index()
    #figure 3
    fig6=px.line(top_5_publisher_update.loc[top_5_publisher_update['Region']=='Global_Sales'],x = 'Year', y='Sales',color='Publisher')
    
    fig6.update_layout(
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='#7FDBFF',
            title=go.layout.Title(text="Publisher Sales by Year",font=go.layout.title.Font(size=20))
    )

    return fig6

@app.callback(
    dash.dependencies.Output('table4', 'children'),
    dash.dependencies.Input('fig-top20', 'hoverData'))
def update_table(hoverData):
    gamename1 = hoverData['points'][0]['y']
    subdf1 = df_remarks.loc[df_remarks['Name']==gamename1]
#     print(subdf1)
    return(dash_table.DataTable(
                                style_data={
                                    'color': '#7FDBFF',
                                    'backgroundColor': '#111111'
                                },
                                style_header={
                                    'backgroundColor': '#111111',
                                    'color': '#7FDBFF',
                                    'fontWeight': 'bold'
                                },
                                data=subdf1.to_dict('rows'),
                                columns=[{'name':i,'id':i} for i in subdf1.columns],
                                #style_cell={}
                                style_cell={
                                    'textAlign': 'center',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': 0,
                                },
                                tooltip_data=[
                                    {
                                        column: {'value': str(value), 'type': 'markdown'}
                                        for column, value in row.items()
                                    } for row in subdf1.to_dict('records')
                                ],
    tooltip_duration=None))
    
@app.callback(
    dash.dependencies.Output('Sales_of_Game', 'figure'),
    dash.dependencies.Input('fig-top20', 'hoverData'))
def update_graph(hoverData):
    gamename = hoverData['points'][0]['y']
#     print(hoverData)
#     print(gamename)
#     subdf = game.loc[game['Name']==gamename]
    subdf = game.loc[game['Name']==gamename]
    subdf = subdf.replace('Global_Sales',np.NaN).dropna(subset=['Region'])
    plot = px.bar(subdf, x='Region', y='Sales')
    plot.update_layout(title='Global Sales Detail:'+gamename,
    plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font_color='#7FDBFF',)
    return plot

#box2
@app.callback(
    Output('Box2', 'figure'),
    Input('Box2_dropdown', 'value'))
def update_box2(platform):
    box2_figure = {
        "data": [
            {
                "type": "indicator",
                "value": vgsales.loc[vgsales['Platform']==platform]['Sales'].sum(),
                "number": {"font": {"color": "#7FDBFF"}},
            }
        ],
        "layout": {
            "template": template,
            "height": 200,
            "margin": {"l": 5, "r": 5, "t": 5, "b": 5},
        },
}
    return box2_figure

#box3
@app.callback(
    Output('Box3', 'figure'),
    Input('Box3_dropdown', 'value'))
def update_box3(publisher):
    box3_figure = {
        "data": [
            {
                "type": "indicator",
                "value": vgsales.loc[vgsales['Publisher']==publisher]['Sales'].sum(),
                "number": {"font": {"color": "#7FDBFF"}},
            }
        ],
        "layout": {
            "template": template,
            "height": 200,
            "margin": {"l": 5, "r": 5, "t": 5, "b": 5},
        },
}
    return box3_figure

if __name__ == '__main__':
    app.run_server(debug=True)