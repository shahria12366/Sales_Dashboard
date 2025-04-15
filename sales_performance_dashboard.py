import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title='Bayut & Dubizzle Sales Dashboard', layout='wide')
st.title('📊 Bayut & Dubizzle Commercial Analytics Dashboard - Jun 2024')

def format_num(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000}M'
        return f'{round(num / 1000000, 1)}M'
    return f'{num // 1000}K'

def main():

    df = pd.read_csv("bayut_dummy_data.csv")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    revenue_val = format_num(df['Total Revenue (AED)'].iloc[-1])
    kpi1.metric(label='💰 Total Revenue (AED)', value=revenue_val)
    kpi2.metric(label='🆕 New Agents', value=df['New Agents'].iloc[-1])
    kpi3.metric(label='📉 Churn Rate (%)', value=df['Churn Rate (%)'].iloc[-1])
    kpi4.metric(label='🔄 Lead Conversion Rate (%)', value=df['Lead Conversion Rate (%)'].iloc[-1])

    # Revenue & New Agents with Secondary Axis
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df['Month'], y=df['Total Revenue (AED)'], name='Total Revenue (AED)', yaxis='y', marker_color='blue'))
    fig1.add_trace(go.Scatter(x=df['Month'], y=df['New Agents'], name='New Agents', yaxis='y2', marker_color='red', mode='lines+markers'))
    fig1.update_layout(
        title='💵 Revenue & New Agent Growth',
        yaxis=dict(title='Total Revenue (AED)', side='left', showgrid=False),
        yaxis2=dict(title='New Agents', side='right', overlaying='y', showgrid=False),
        legend=dict(orientation="h", y=-0.2),
        barmode='group'
    )

    # Churn Rate Trend (Line Chart)
    fig2 = px.line(df, x='Month', y='Churn Rate (%)', title='📉 Agent Churn Rate Over Time', markers=True)
    fig2.update_traces(line=dict(color='orange'))

    # Market Share (Pie Chart)
    fig3 = px.line(df, x='Month', y='Market Share (%)', title='📉 Market Share Over Time', markers=True)
    fig3.update_traces(line=dict(color='blue'))

    # Lead Conversion (Funnel Chart)
    fig4 = go.Figure(go.Funnel(
        y=['Visitors', 'Leads', 'Qualified Leads', 'Clients'],
        x=[1550, 775, 310, 124],
        textinfo='value+percent initial'
    ))
    fig4.update_layout(title='🔄 Lead Conversion Funnel')

    # Layout
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True, border=True)
    col2.plotly_chart(fig2, use_container_width=True, border=True)

    col3, col4 = st.columns(2)
    col3.plotly_chart(fig3, use_container_width=True, border=True)
    col4.plotly_chart(fig4, use_container_width=True, border=True)

main()

