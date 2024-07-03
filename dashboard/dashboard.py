import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#mengubah style seaborn
sns.set(style='dark')

#mengimport data
all_data = pd.read_csv('main_data.csv')

datetime_columns = ['dteday']
all_data.sort_values(by='dteday', inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

#menyiapkan dataframe yang diperlukan
def create_month_recap(df):
    plot_month = df['mnth'].astype(str)
    plot_year = df['yr'].astype(str)
    df['year_month'] = plot_month + ' ' + plot_year
    df['total_sum'] = df.groupby('year_month')['cnt'].transform('sum')
    return df[['year_month', 'total_sum']]

def create_season_recap(df):
    season_recap = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_recap

def create_weather_recap(df):
    weather_recap = df.groupby(by='weathersit').agg({
    'cnt': 'mean'
    }).reset_index()
    return weather_recap

def create_workingday_hour_recap(df):
    filter_workingday = df[(df['workingday'] == 'weekday')]
    workingday_hour_recap = filter_workingday.groupby(by='hr').agg({
    'cnt': 'sum'
    }).reset_index()
    return workingday_hour_recap

def create_holiday_hour_recap(df):
    filter_holiday = df[(df['holiday'] == 1)|(df['workingday'] == 'weekend')]
    holiday_hour_recap = filter_holiday.groupby(by='hr').agg({
    'cnt': 'sum'
    }).reset_index()
    return holiday_hour_recap

def create_daily_recap(df):
    daily_recap = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_recap

def create_registered_recap(df):
    registered_recap = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_recap

def create_casual_recap(df):
    casual_recap = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_recap

def create_temp_recap(df):
    temp_recap = df.groupby(by='dteday').agg({
        'temp': 'mean'
    }).reset_index()
    return temp_recap

def create_hum_recap(df):
    hum_recap = df.groupby(by='dteday').agg({
        'hum': 'mean'
    }).reset_index()
    return hum_recap

#membuat filter tanggal pada sidebar
max_date = pd.to_datetime(all_data['dteday']).dt.date.max()
min_date = pd.to_datetime(all_data['dteday']).dt.date.min()

with st.sidebar:
    

    #input start_date dan end_date
    start_date, end_date = st.date_input(
        label='Pilih  Rentang Waktu',
        max_value=max_date,
        min_value=min_date,
        value=[min_date, max_date]
    )
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)
    
    
    st.title ('Made by:')
    st.write(
        """ 
     
        Nama            : **Martin Ompusunggu**\n
        Dicoding Id     : **martinexe4**\n
        Email           : **restuwaisnawa@gmail.com**
 
        """
    )

main_df = all_data[(all_data['dteday'] >= str(start_date)) & 
                (all_data['dteday'] <= str(end_date))]

month_recap_df = create_month_recap(main_df)
season_recap_df = create_season_recap(main_df)
weather_recap_df = create_weather_recap(main_df)
workingday_hour_recap_df = create_workingday_hour_recap(main_df)
holiday_hour_recap_df = create_holiday_hour_recap(main_df)
daily_recap_df = create_daily_recap(main_df)
casual_recap_df = create_casual_recap(main_df)
registered_recap_df = create_registered_recap(main_df)
temp_recap_df = create_temp_recap(main_df)
hum_recap_df = create_hum_recap(main_df)

#Membuat UI
st.header('BIKE SHARING ANALYSIS DASHBOARD')

#Subheader Rent Summary
st.subheader('Bike Rent Summary')
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    daily_recap = daily_recap_df['cnt'].sum()
    st.metric('Total User', value= daily_recap)

with col2:
    registered_recap = registered_recap_df['registered'].sum()
    st.metric('Registered User', value= registered_recap)

with col3:
    casual_recap = casual_recap_df['casual'].sum()
    st.metric('Casual User', value= casual_recap)

with col4:
    temp_recap = temp_recap_df['temp'].mean()
    st.metric('Mean Temperature', value= temp_recap)

with col5:
    hum_recap = hum_recap_df['hum'].mean()
    st.metric('Mean Humidity', value= hum_recap)

#Subheader Monthly Recap
st.subheader('Monthly Rent Recap')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_recap_df['year_month'],
    month_recap_df['total_sum'],
    marker='o', 
    linewidth=5,
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)

st.pyplot(fig)

#Subheader Season and Weather Recap
st.subheader('Season and Weather Recap')
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y='registered', 
        x='season',
        data=season_recap_df.sort_values(by='registered', ascending=False),
        color='tab:blue',
        label='Registered User',
        ax=ax
    )
    sns.barplot(
        y='casual', 
        x='season',
        data=season_recap_df.sort_values(by='casual', ascending=False),
        color='tab:orange',
        label='Casual User',
        ax=ax
    )
    ax.set_title('Number of Rent by Season', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.legend(fontsize=20)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y='cnt', 
        x='weathersit',
        data=weather_recap_df.sort_values(by='cnt', ascending=False),
        ax=ax
    )
    
    ax.set_title('Mean of Rent by Weather', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

#Subheader Workingday and Holiday Hour Recap
st.subheader('Workingday and Holiday Hour Recap')
 
col1, col2 = st.columns(2)
 
with col1:
    workingday_max_col = workingday_hour_recap_df['cnt'].idxmax()
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y='cnt', 
        x='hr',
        data=workingday_hour_recap_df,
        color='tab:blue',
        ax=ax
    )
    plt.bar(workingday_max_col, workingday_hour_recap_df.loc[workingday_max_col, 'cnt'], color='tab:red', label='Most Rented Hour')
    ax.set_title('Workingday Rent Hour Recap', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.legend(fontsize=20)
    st.pyplot(fig)

with col2:
    holiday_max_col = holiday_hour_recap_df['cnt'].idxmax()
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y='cnt', 
        x='hr',
        data=holiday_hour_recap_df,
        color='tab:blue',
        ax=ax
    )
    plt.bar(holiday_max_col, holiday_hour_recap_df.loc[holiday_max_col, 'cnt'], color='tab:red', label='Most Rented Hour')
    ax.set_title('Holiday Rent Hour Recap', loc='center', fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.legend(fontsize=20)
    st.pyplot(fig)