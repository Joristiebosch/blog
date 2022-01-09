import plotly.express as px
from plotly.subplots import make_subplots

def plot(df,axis_labels=('x','y','var'),hover_labels=('x','y','var'),plot_type='linlin',e_notation=(True,False),x_range=None,y_range=None):
    log_y = plot_type[:3]=='log'
    log_x = plot_type[3:6]=='log'
    
    if hover_labels[2]!='':
        hover_labels=(hover_labels[0],hover_labels[1],hover_labels[2]+': ')
    
    fig = px.line(df,
                  labels = {df.index.name: axis_labels[0],'value': axis_labels[1], 'variable': axis_labels[2]},
                  line_shape='spline',
                  log_x=log_x, log_y=log_y,
                  template = 'plotly_white',
                  render_mode="svg")
        
    fig.update_layout(hoverlabel={'bgcolor': "white", 'font_size': 14})
    
    # Hacky update all traces because can't print trace name I guess
    for trace in fig.data:
        trace['hovertemplate']= '<b>'+hover_labels[2]+trace['name']+'</b><br>'+hover_labels[0]+': %{x}<br>'+hover_labels[1]+': %{y}<br><extra></extra>'
    
    if e_notation[0]:
        fig.update_layout(xaxis={'tickformat':'.2e'})
    if e_notation[1]:
        fig.update_layout(yaxis={'tickformat':'.2e'})
    
    if x_range!=None:
        fig.update_xaxes(range=x_range)
    if y_range!=None:
        fig.update_yaxes(range=y_range)
        
    fig.show()

def filter_plot(spectral_df,  filters_df, mode='',x_axis_range=None,y_axis_range=[0,3500],spectrum_title='Atmospheric Loading'):
    if mode=='box':
        line_shape_filters='hv'
        error_y_spectrum={}
        mode_spectrum='lines'
    elif mode=='stem':
        line_shape_filters='hvh'
        error_y_spectrum={'type':'percent','value':0,'valueminus':100}
        mode_spectrum='markers'
    else:
        line_shape_filters='spline'
        error_y_spectrum={}
        mode_spectrum='lines'
        
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    # Overlay of filters
    fig2 = px.line(filters_df,
                  line_shape=line_shape_filters,
                 labels={'value': 'eta','variable': 'bin [Ghz]'})
    fig2.update_traces(fill='tozeroy')
    
    for trace in fig2.data:
        trace['hovertemplate']= '<b>Bin: '+trace['name']+'</b><br>nu: %{x}<br>eta: %{y}<br><extra></extra>'

    subfig.add_traces(fig2.data)
    subfig.update_traces(secondary_y=False)

    # Signal plot
    subfig.add_scatter(x=spectral_df.index,
                       y=spectral_df,
                       secondary_y=True,
                       mode=mode_spectrum,
                       line_shape='spline')

    subfig.update_traces(showlegend=False,
                         marker={'size':8},
                         error_y=error_y_spectrum,
                         secondary_y=True,
                         hovertemplate='<b>'+spectrum_title+'</b><br>Frequency [GHz]: %{x}<br>Spectral Power: %{y}<extra></extra>')
    
    subfig.layout.xaxis.title="$\\nu\:\mathrm{[GHz]}$"
    subfig.layout.yaxis2.title="$E_{e,\\nu}\:\mathrm{[Jy]}$"

    subfig.layout.yaxis2.range=y_axis_range
    subfig.layout.yaxis1.range=[0,1]
    if x_axis_range != None:
        subfig.layout.xaxis.range=x_axis_range

    subfig.layout.yaxis2.side='left'
    subfig.layout.yaxis1.showticklabels=False

    subfig.layout.template='plotly_white'
    subfig.layout.hoverlabel = {'bgcolor': "white", 'font_size': 14}

    subfig.show()