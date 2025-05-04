import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Bayut and Dubizzle Listings Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

def format_num(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 2)} M'
    elif num > 1000:
        return f'{round(num / 1000,2)} K'
    else:
        return round(num,2)

def main():

    df = pd.read_csv("data_for_dashboard.csv")
    df = df[df['outlier_flag']=='Normal']
    with st.sidebar:
        st.title("Bayut and Dubizzle Listings Dashboard")
        month_list = list(df['month_posted'].unique())
        month_list.append('All - Apr, May & Jun 2020')
        selected_month= st.selectbox('Select a month', month_list, index=len(month_list)-1)
        if selected_month != 'All - Apr, May & Jun 2020':
            df_present = df[df['month_posted'] == selected_month]
        else:
            df_present = df
        category_list = sorted(list(df['category_name_an'].unique()))
        category_list[-1] = 'All'
        selected_category= st.selectbox('Select a category', category_list, index=len(category_list)-1)
        if selected_category!='All':
            df_present = df_present[df_present['category_name_an'] == selected_category]
        min_price = 0
        max_value = int(df_present['listing_price'].max())
        min_price, max_price = st.slider(
        'Select Price Range:',
        min_value=int(df['listing_price'].min()),
        max_value=int(df['listing_price'].max()),
        value=(int(df['listing_price'].min()), int(df['listing_price'].max())),
        step=10
        )
    df_present = df_present[(df_present['listing_price'] >= min_price) & (df_present['listing_price'] <= max_price)]
        
    col = st.columns((0.2, 0.2, 0.2, 0.2, 0.2), gap='small')
    with col[0]:
        with st.container(border=True):
            #total_listings = df_present['listing_sk'].nunique()
            total_listings = df_present['listing_sk'].count()
            st.metric(label='Total Listings', value=format_num(total_listings))
    with col[1]:
        with st.container(border=True):
            total_users = df_present['user_sk'].nunique()
            st.metric(label='Total Users', value=format_num(total_users))
    with col[2]:
        with st.container(border=True):
            avg_listing_price = df_present['listing_price'].mean()
            st.metric(label='Avg Listing Price (AED)', value=format_num(avg_listing_price))
    with col[3]:
        with st.container(border=True):
            listings_per_user = total_listings/total_users
            st.metric(label='Avg Listings Per User', value=format_num(listings_per_user))
    with col[4]:
        with st.container(border=True):
            gmv = df_present['listing_price'].sum()
            st.metric(label='GMV (AED)', value=format_num(gmv))
            
    charts_col = st.columns((0.7, 0.3), gap='medium')
    with charts_col[0]:
        with st.container(border=True):
            df_present['time_posted_local'] = pd.to_datetime(df_present['time_posted_local'], errors='coerce', format='%d/%m/%y')
            df_present['date'] = df_present['time_posted_local'].dt.date
            listing_count_df = df_present.groupby('date')['listing_sk'].count().reset_index()
            fig = px.line(
            listing_count_df,
            x='date',
            y='listing_sk',
            labels={'date': 'Posting Date', 'listing_sk': 'Number of Listings'},
            title = 'Listings Created')
            st.plotly_chart(fig, use_container_width=True)
        
        with st.container(border=True):
            bins = [0, 500, 1000, 1500, max_value]
            labels = ['0-500', '500-1000', '1000-1500', '>1500']
            df_present['price_bucket'] = pd.cut(df_present['listing_price'], bins=bins, labels=labels, right=False)
            price_group = df_present.groupby('price_bucket')['listing_sk'].count().reset_index()
            price_group.rename(columns={'listing_sk': 'total_listings'}, inplace=True)
            fig = px.bar(
                price_group,
                x='price_bucket',
                y='total_listings',
                labels={'price_bucket': 'Price Range (AED)', 'total_listings': 'Total Listings'},
                color='total_listings',
                title='Total Listings by Price Range'
            )
            st.plotly_chart(fig, use_container_width=True)
    with charts_col[1]:
        with st.container(border=True):
            category_group = df.groupby('category_name_an')['listing_sk'].count().reset_index()
            category_group.rename(columns={'listing_sk': 'total_listings'}, inplace=True)
            fig = px.pie(
                category_group,
                values='total_listings',
                names='category_name_an',
                title='Listings Across Categories',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
            legend=dict(
                orientation='h',  
                yanchor='top',    
                y=-0.3,           
                xanchor='center', 
                x=0.5             
            ))
            st.plotly_chart(fig, use_container_width=True)

main()
