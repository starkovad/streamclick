import streamlit as st
from apis import Api, Oanda
from clickhouse_driver import Client

import plotly.graph_objects as go

import pandas as pd

def inst_interface(key, current_inst_type, insts, granularity):

    if key in current_inst_type:
        key = key.lower()
        current_instrument = st.sidebar.selectbox(f'{key}', insts, key=key)

        if current_instrument:
            g = st.selectbox('Choose granularity: ', granularity, key=key)

            if g:
                ans = clk.execute(f''' select datetime, price from oanda.{key}_{g} where inst='{current_instrument}' ''')
                ans = pd.DataFrame(ans, columns = ['date', 'price'])

                ans.set_index('date', inplace=True)

                layout = go.Layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis={'title':'Datetime'},
                    yaxis={'title':'Price'},
                    font={'size': 19, 'color': "#7f7f7f"},
                    title=f'{g} {key} {current_instrument} Prices',
                    xaxis_tickformat='%d %B (%a)<br>%Y',
                    title_font_size=30,
                    )

                trace1 = go.Scatter(x = ans.index,
                                    y = ans['price'],
                                    marker = {'color': 'black', 'size': 2},
                                    line = {'width': 2},
                                    mode='lines',
                                    name='Real data'
                                    )

                if ans.shape[0]:
                    period = st.slider('Select MA Period', 1, 30, 5, format=None,key=key)
                    st.subheader('Current Window Size %s days' % period)

                    ans['MA'] = ans.rolling(period).mean()

                    trace2 = go.Scatter(x = ans.index,
                                        y = ans['MA'],
                                        fill='tonexty',
                                        marker={'color': 'rgba(246, 38, 129, 250)'},
                                        mode='lines',
                                        name='Simple Moving Average'
                                        )

                    traces = [trace1, trace2]
                else:
                    traces = trace1
                
                fig = dict(data=traces, layout=layout)

                st.plotly_chart(fig, width=1200, height=500)
    
@st.cache
def inst_info(inst_type):

    query = '''select inst
                from oanda.inst_info
                where type=%(type)s '''

    instruments = clk.execute(query,
                            params={'type': inst_type})

    return [instrument[0] for instrument in instruments]

if __name__ == '__main__':
    clk = Client('click-server', port=9000)

    instrument_types = clk.execute('select distinct type from oanda.inst_info')
    current_inst_type = st.sidebar.multiselect('Select Instrument Type: ',
                                        [i[0] for i in instrument_types])
    
    granularity = ['M2', 'M3', 'M4', 'M5', 'M10', 'M15', 'M30', 'H1']

    metal_inst = inst_info('METAL')
    currency_inst = inst_info('CURRENCY')
    cfd_inst = inst_info('CFD')
    
    inst_interface('METAL', current_inst_type, metal_inst, granularity)
    inst_interface('CURRENCY', current_inst_type, currency_inst, granularity)
    inst_interface('CFD', current_inst_type, currency_inst, granularity)