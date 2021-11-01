# Graphs
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from parameters import df


# Credits versus Debits for Each month
# This graph shows the daily trend of the transaction amount for both debits and credits, for the full period.

def amount_trend():
    annotations = []

    fig = px.bar(df, x="trns_date", y="amount_cleaned", color='cr_dr_ind')

    fig.layout.update(barmode='stack',bargap=0,bargroupgap=0)

    fig.layout.update(plot_bgcolor='white')

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Transaction Debits & Credits NAD value',
                              font=dict(family='Arial',
                                        size=14,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.95, y=-0.2,
                              xanchor='center', yanchor='top',
                              text='',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

    fig.update_layout(annotations=annotations,xaxis_tickangle=-45)
    fig.update_xaxes(ticks="inside",nticks=20,tickwidth=1, tickcolor='#eee4e4')
    return fig

#amount_trend()

# Daily Balance Trend
# This graph shows the daily balance for the full period.

def balance_trend():
    annotations = []
    fig = px.line(df, x="trns_date", y="balance_cleaned"
                    )
    fig.layout.update(plot_bgcolor='white')

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Trend of Daily Balance',
                              font=dict(family='Arial',
                                        size=14,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.95, y=-0.6,
                              xanchor='center', yanchor='top',
                              text='',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

    fig.update_layout(annotations=annotations,xaxis_tickangle=-45)
    fig.update_xaxes(ticks="inside",nticks=20,tickwidth=1, tickcolor='#eee4e4',rangeslider_visible=True)
    return fig

#balance_trend()

# Debits Transaction Type Category Preference
# Proportionally see which transaction type is most preferred.

def trns_preference():
    ### Category Preference
    pyo.init_notebook_mode()

    figure = go.Figure()
    annotations = []
    months = list(set(df.month_year.tolist()))

    month_color = {
        '2020-06': '#002366',
        '2020-07': '#ED2124'
                    }
    for month in months:
        color = month_color.get(month)
        #highlight = color != 'black'
        data_filtered = df[(df.month_year == month) & (df.cr_dr_ind=='DR')]
        plot_data = data_filtered.groupby(['trns_type'], as_index=False).Count.sum()
        axis = plot_data.trns_type.tolist()
        axis.append(axis[0])
        plot_data = plot_data.Count.tolist()
        plot_data = (np.array(plot_data) / sum(plot_data) * 100).tolist()
        plot_data.append(plot_data[0])
        figure.add_trace(
            go.Scatterpolar(
                r=plot_data,
                theta=axis,
                showlegend=True,
                name=month,
                hoverinfo='name+r',
                hovertemplate='%{r:0.0f}%',
                mode='lines',
                line_color=color,
                #opacity=0.8 if highlight else 0.25,
                line_shape='spline',
                line_smoothing=0.8,
                #line_width=1.6 if highlight else 0.6
            )
        )

    title = 'Proportionally which debit transaction types does the borrower lean more towards?.' \
            '<br><span style="font-size:10px"><i>Select a specific month ' \
            'to view the trend</span></i>'

    figure.update_layout(
        title_text = title,
        title_font_color = '#333333',
        title_font_size = 16,
        polar_bgcolor='white',
        polar_radialaxis_visible=True,
        polar_radialaxis_showticklabels=True,
        polar_radialaxis_tickfont_color='darkgrey',
        polar_angularaxis_color='grey',
        polar_angularaxis_showline=False,
        polar_radialaxis_showline=False,
        polar_radialaxis_layer='below traces',
        polar_radialaxis_gridcolor='#F2F2F2',
        #polar_radialaxis_range=(0,55),
        polar_radialaxis_tickvals=[25, 50],
        polar_radialaxis_ticktext=['25%', '50%'],
        polar_radialaxis_tickmode='array',

        legend_font_color = 'grey', # We don't want to draw attention to the legend
        legend_itemclick = 'toggleothers', # Change the default behaviour, when click select only that trace
        legend_itemdoubleclick = 'toggle', # Change the default behaviour, when double click ommit that trace
    #     width = 800, # chart size
    #     height = 500 # chart size
    )

    annotations.append(dict(xref='paper', yref='paper', x=0.95, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    figure.update_layout(annotations=annotations)
    return figure

#trns_preference()

# Debits Transaction by merchant category
# Proportionally see which merchant category the customer leans more towards.
def merch_preference():
    ### Category Preference
    pyo.init_notebook_mode()

    figure = go.Figure()
    annotations = []
    months = list(set(df.month_year.tolist()))

    month_color = {
        '2020-06': '#E9C46A',
        '2020-07': '#ED2124'
                    }
    for month in months:
        color = month_color.get(month)
        #highlight = color != 'black'
        data_filtered = df[(df.month_year == month) & (df.cr_dr_ind=='DR')]
        plot_data = data_filtered.groupby(['merchant_category'], as_index=False).Count.sum()
        axis = plot_data.merchant_category.tolist()
        axis.append(axis[0])
        plot_data = plot_data.Count.tolist()
        plot_data = (np.array(plot_data) / sum(plot_data) * 100).tolist()
        plot_data.append(plot_data[0])
        figure.add_trace(
            go.Scatterpolar(
                r=plot_data,
                theta=axis,
                showlegend=True,
                name=month,
                hoverinfo='name+r',
                hovertemplate='%{r:0.0f}%',
                mode='lines',
                line_color= color,
                #opacity=0.8 if highlight else 0.25,
                line_shape='spline',
                line_smoothing=0.8
                #line_width=1.6 if highlight else 0.6
            )
        )

    title = 'Proportionally which merchant category does the borrower lean more towards?.' \
            '<br><span style="font-size:10px"><i>Select a specific month ' \
            'to view the trend</span></i>'

    figure.update_layout(
        title_text = title,
        title_font_color = '#333333',
        title_font_size = 16,
        polar_bgcolor='white',
        polar_radialaxis_visible=True,
        polar_radialaxis_showticklabels=True,
        polar_radialaxis_tickfont_color='darkgrey',
        polar_angularaxis_color='grey',
        polar_angularaxis_showline=False,
        polar_radialaxis_showline=False,
        polar_radialaxis_layer='below traces',
        polar_radialaxis_gridcolor='#F2F2F2',
        #polar_radialaxis_range=(0,55),
        polar_radialaxis_tickvals=[25, 50],
        polar_radialaxis_ticktext=['25%', '50%'],
        polar_radialaxis_tickmode='array',

        legend_font_color = 'grey', # We don't want to draw attention to the legend
        legend_itemclick = 'toggleothers', # Change the default behaviour, when click select only that trace
        legend_itemdoubleclick = 'toggle', # Change the default behaviour, when double click ommit that trace
    #     width = 800, # chart size
    #     height = 500 # chart size
    )
    annotations.append(dict(xref='paper', yref='paper', x=0.95, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    figure.update_layout(annotations=annotations)
    return figure
#merch_preference()
