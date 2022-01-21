import plotly.express as px
from plotly.subplots import make_subplots

def plot(df,axis_labels=('x','y','var'),hover_labels=('x','y','var'),plot_type='linlin',e_notation=(False,False),x_range=None,y_range=None, mode='lines', legendgroup=None, fill='none', line_shape='spline'):
    log_y = plot_type[:3]=='log'
    log_x = plot_type[3:6]=='log'
    
    if hover_labels[2]!='':
        hover_labels=(hover_labels[0],hover_labels[1],hover_labels[2]+': ')
    
    fig = px.line(df,
                  labels = {df.index.name: axis_labels[0],'value': axis_labels[1], 'variable': axis_labels[2]},
                  line_shape=line_shape,
                  log_x=log_x, log_y=log_y,
                  template = 'plotly_white',
                  render_mode="svg")
    
    fig.update_traces(fill=fill)
    fig.update_layout(hoverlabel={'bgcolor': "white", 'font_size': 14})
    
    # Hacky update all traces because can't print trace name I guess
    for idx, trace in enumerate(fig.data):
        trace['hovertemplate']= '<b>'+hover_labels[2]+trace['name']+'</b><br>'+hover_labels[0]+': %{x}<br>'+hover_labels[1]+': %{y}<br><extra></extra>'
        if legendgroup is not None:
            trace.legendgroup=legendgroup[idx]
            trace.legendgrouptitle.text=legendgroup[idx]
    
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
        error_y_spectrum={'type':'percent','value':0,'valueminus':200}
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
    
    # Switch axis label sides
    subfig.layout.yaxis2.side='left'
    subfig.layout.yaxis1.showticklabels=False
    
    # Change template to thesis
    subfig.layout.template='plotly_white'
    subfig.layout.hoverlabel = {'bgcolor': "white", 'font_size': 14}

    subfig.show()
   
def psd_overlay(data, psd_underlay,var_axis='var',var_hover='var',x_axis_range=None,y_axis_range=None,overlay_title='PSD at KID', show_legend_underlay=True):       
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add psd plot
    fig_under= px.line(psd_underlay,
                      line_shape='spline')
    
    fig_under.update_traces(showlegend=show_legend_underlay,
                           line={'color': 'rgba(127,127,127,0.3)'},
                           hovertemplate='<b>'+overlay_title+'</b><br>nu [GHz]: %{x:.2f}<br>PSD [W/Hz]: %{y:.ef}<extra></extra>')
    
    
    
    # Add signal plots
    for signal, name, mode, customdata, visible, legendgroup in data:
        if customdata is None:
            hovertemplate='<b>'+name+'</b><br>nu [GHz]: %{x:.2f}<br>'+var_hover+': %{y:.2e}<extra></extra>'
        else:
            hovertemplate='<b>'+name+'</b><br>nu [GHz]: %{x:.2f}<br>'+var_hover+': %{y:.2e}<br>R: %{customdata[0]:.0f}<br>Transmission: %{customdata[1]:.3f}<br>Chi Square: %{customdata[2]:.2e} <extra></extra>'
        subfig.add_scatter(x=signal.index,
                         y=signal.values,
                         mode=mode,
                           visible=visible,
                           customdata=customdata,
                         hovertemplate=hovertemplate,
                            name=name,
                           line_shape='spline',
                          secondary_y=True)
        if legendgroup is not None:
            trace = subfig.data[-1]
            trace.legendgroup=legendgroup
            trace.legendgrouptitle.text=legendgroup
            
        
    subfig.add_traces(fig_under.data)
    
    subfig.layout.xaxis.title="$\\nu\:\mathrm{[GHz]}$"
    subfig.layout.yaxis2.title=var_axis
    subfig.layout.yaxis1.title="$\mathrm{PSD\:[W\:Hz^{-1}]}$"
    
    # Switch axis label sides
    subfig.layout.yaxis2.side='left'
    subfig.layout.yaxis1.side='right'
    #subfig.layout.yaxis1.showticklabels=False
    
    # Set axis range
    if y_axis_range is not None:
        subfig.layout.yaxis2.range=y_axis_range
    if x_axis_range is not None:
        subfig.layout.xaxis.range=x_axis_range
    
    # Change template to thesis
    subfig.layout.template='plotly_white'
    subfig.layout.hoverlabel = {'bgcolor': "white", 'font_size': 14}
    subfig.show()