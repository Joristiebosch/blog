import plotly.express as px
from IPython.display import HTML
HTML(fig.to_html())

def plot(df,x_label='x',y_label='y',line_label='var',plot_type='linlin',e_notation=(True,False),x_range=None,y_range=None):
    log_y = plot_type[:3]=='log'
    log_x = plot_type[3:6]=='log'
    
    fig = px.line(df,
                  labels = {df.index.name: x_label,'value': y_label, 'variable': line_label},
                  line_shape='spline',
                  log_x=log_x, log_y=log_y,
                  template = 'plotly_white',
                  render_mode="svg")
        
    fig.update_layout(hoverlabel={'bgcolor': "white", 'font_size': 14})
    
    if e_notation[0]:
        fig.update_layout(xaxis={'tickformat':'.2e'})
    if e_notation[1]:
        fig.update_layout(yaxis={'tickformat':'.2e'})
    
    if x_range!=None:
        fig.update_xaxes(range=x_range)
    if y_range!=None:
        fig.update_yaxes(range=y_range)
        
    HTML(fig.to_html())
