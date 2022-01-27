import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import seaborn as sns

st.set_page_config(page_title = "Road Safety Data",
page_icon="bar_chart",
layout="wide")

###--- Read in data
df = pd.read_csv('df_london.csv')
df_all = pd.read_csv('df_all_data_london.csv')
# Create column with hour
df['hours'] = pd.DatetimeIndex(df['time']).hour

###--- SIDEBAR
# Select year
year = st.sidebar.multiselect(
     "Select year:",
     df['year'].unique(),
     default=2015
     )

# Select month
container = st.sidebar.container()
all = st.sidebar.checkbox("Select all months")
if all:
    month = container.multiselect("Select month:",
         df['month'].unique(),df['month'].unique())
else:
    month =  container.multiselect("Select month:",
        df['month'].unique())

# Select day of week
container = st.sidebar.container()
all = st.sidebar.checkbox("Select all days of the week")
if all:
    week = container.multiselect("Select day of the week:",
         df['day_of_week'].unique(),df['day_of_week'].unique())
else:
    week =  container.multiselect("Select day of the week:",
        df['day_of_week'].unique())

# # Select hours
# hours = st.sidebar.slider(
#      'Select a range of hours:',
#      0, 23, (19, 23))

# Select accident severity
severity = st.sidebar.multiselect(
     "Select severity of accident:",
     df['accident_severity'].unique(),
     default='Fatal'
     )

# Select district
container = st.sidebar.container()
all = st.sidebar.checkbox("Select all districts")
if all:
    districts = container.multiselect("Select district:",
         df['local_authority_district'].unique(),df['local_authority_district'].unique())
else:
    districts =  container.multiselect("Select district:",
        df['local_authority_district'].unique())

###--- MAIN PAGE
st.title(":bar_chart:  Road Safety Data")
st.markdown("##")

# Query data from selected options
df_selection = df.query(
        "year == @year & \
            accident_severity == @severity &\
                local_authority_district == @districts &\
                    month == @month & \
                         day_of_week == @week"
)
df_selection_all = df_all.query(
        "year == @year & \
            accident_severity == @severity &\
                local_authority_district == @districts &\
                    month == @month & \
                         day_of_week == @week"
)

### Map
fig = px.density_mapbox(df_selection, lat = 'latitude', lon = 'longitude',
                       z = 'severity', radius = 10,
                       center = dict(lat = 51.5, lon = -0.1),
                       #zoom = 1,
                       hover_name = 'local_authority_district',
                       mapbox_style="stamen-terrain",
                       title = 'Severity',
                       width=600, height=800)
fig.update_layout(mapbox_center_lat=50)
st.plotly_chart(fig, use_container_width=True)


### Time Series
fig = px.bar(df_selection, x='date', y="severity")
st.plotly_chart(fig, use_container_width=True)

### Bar plots

# cars per hour
st.header('Number of accidents per hour')
hour_accident_df = df_selection['hours'].value_counts()
fig = px.bar(hour_accident_df)
st.plotly_chart(fig, use_container_width=True)

#histogram
st.header('Accident severity by district')
df_bars = df_selection.groupby(['local_authority_district','year'])['accident_severity_inv'].sum().reset_index()
fig = px.histogram(df_bars, x='local_authority_district', y='accident_severity_inv', color='year', barmode='group',
labels={ "accident_severity_inv": "Accident severity",
"local_authority_district": "District"})
st.plotly_chart(fig, use_container_width=True)

st.header('Number of casualties by district')
df_bars = df_selection.groupby(['local_authority_district','year'])['number_of_casualties'].sum().reset_index()
fig = px.histogram(df_bars, x='local_authority_district', y='number_of_casualties', color='year', barmode='group',
labels={ "number_of_casualties": "Number of casualties" ,
"local_authority_district": "District"})
st.plotly_chart(fig, use_container_width=True)

st.header('Severity by district')
df_bars = df_selection.groupby(['local_authority_district','year'])['severity'].sum().reset_index()
fig = px.histogram(df_bars, x='local_authority_district', y='severity', color='year', barmode='group',
labels={ "severity": "Severity",
"local_authority_district": "District" })
st.plotly_chart(fig, use_container_width=True)

# Histogram
st.header('Distribution of cumber of casualties')
x1 = df_selection[['number_of_casualties', 'year']]
fig = px.histogram(x1, x="number_of_casualties", color = 'year')
st.plotly_chart(fig, use_container_width=True)

# Pie charts
fig = px.pie(df_selection_all, values='number_of_vehicles', names='accident_severity', title='Number of vehicles by accident severity')
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(df_selection_all, values='number_of_vehicles', names='sex_of_driver', title = 'Number of vehicles by sex of driver')
st.plotly_chart(fig, use_container_width=True)

fig = px.pie(df_selection_all, values='number_of_vehicles', names='age_band_of_driver', title = 'Number of vehicles by age of driver')
st.plotly_chart(fig, use_container_width=True)

100*df_selection_all.pivot_table('severity', index='day_of_week', 
columns='year', aggfunc='sum')/df_selecdf_selection_alltion.pivot_table('severity', index='day_of_week', columns='year', aggfunc='sum').sum()

100*df_selection_all.pivot_table('severity', index='month', columns='year',
 aggfunc='sum')/df_selection_all.pivot_table('severity', index='month', columns='year', aggfunc='sum').sum()


st.image("images\cars1.jpg")
st.image("images\cars2.jpg")
st.image("images\cars3.jpg")
st.image("images\cars4.jpg")
st.write("Images from DailyMail.com https://www.dailymail.co.uk/news/article-9684205/Pall-Mall-misery-Dozens-boy-racers-cause-chaos-central-London-Maseratis-Mercedes.html")

