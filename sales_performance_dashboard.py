import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Bayut and Dubizzle Monthly Sales Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

def format_num(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000}M'
        return f'{round(num / 1000000, 1)}M'
    return f'{round(num // 1000,1)}K'

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Date", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

def main():

    df = pd.read_csv("data_for_dashboard.csv")
    with st.sidebar:
        st.title('Bayut and Dubizzle Monthly Sales Dashboard')
        month_list = list(df['month_posted'].unique())[::-1]
        selected_month= st.selectbox('Select a month', month_list, index=len(month_list)-1)
        df_present = df[df['month_posted'] == selected_month]
        df_prev = df[df['month_posted'] == selected_month-1]

        
    col = st.columns((0.2, 0.2, 0.2, 0.2, 0.2), gap='medium')
    with col[0]:
        with st.container(border=True):
            st.markdown('#### Total Listings')
            total_listings = df_present['listing_sk'].nunique()
            total_listings_prev_month = int(df_prev['listing_sk'].nunique())
            st.metric(label='', value=format_num(total_listings), delta=total_listings_prev_month)
    with col[1]:
        with st.container(border=True):
            st.markdown('#### Total Users')
            total_users = df_present['user_sk'].nunique()
            total_users_prev_month = int(df_prev['user_sk'].nunique())
            st.metric(label='', value=format_num(total_users), delta=total_users_prev_month)
    with col[2]:
        with st.container(border=True):
            new_users_list = []
            present_users_list = df_present['user_sk'].unique()
            prev_users_list = df_prev['user_sk'].unique()
            for x in present_users_list:
                if x not in prev_users_list:
                    new_users_list.append(x)
            new_users = len(set(new_users_list))
            st.markdown('#### New Users')
            st.metric(label='', value=format_num(new_users))
    with col[3]:
        with st.container(border=True):
            avg_listing_price = df_present['listing_price'].mean()
            avg_listing_price_prev = df_prev['listing_price'].mean()
            st.markdown('#### Avg Listing Price')
            st.metric(label='', value=format_num(avg_listing_price))
    with col[4]:
        with st.container(border=True):
            listings_per_user = round(total_listings/total_users,1)
            st.markdown('#### Listings Per User')
            st.metric(label='', value=listings_per_user)
            
            

main()
