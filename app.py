"""
Visualizing Towed vehicles in Montreal

Author: Louis Willems https://github.com/louiswillems
Original Source: https://github.com/louiswillems/Towed-vehicles-in-Montreal/blob/master/app.py
"""


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.image("images/logo_montreal.png", use_column_width=True)


st.title("Visualizing towed vehicles in the city of Montreal 🚗")

st.markdown("<br><br>", unsafe_allow_html=True) 

st.write("The [data](https://data.montreal.ca/dataset/1d785ef8-f883-47b5-bac5-dce1cdddb1b0/resource/65dd096f-7296-40e8-8cfe-e26b928bcce5/download/remorquages.csv) show vehicles towed by the City of Montreal since 2016. Towing is performed for example during snow removal, construction work or during special events.")

st.write("Use **filters** to pick a specific **Year**, **Month**, **Day** and **Hour** and explore the data. [See source code](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py)")

st.markdown("<br>", unsafe_allow_html=True) 

st.markdown("<div align='center'><br>"
                "<img src='https://img.shields.io/badge/MADE%20WITH-PYTHON%20-red?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/SERVED%20WITH-Heroku-blue?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/DASHBOARDING%20WITH-Streamlit-green?style=for-the-badge'"
                "alt='API stability' height='25'/></div>", unsafe_allow_html=True)

@st.cache
def load_data():

    data = pd.read_csv('https://data.montreal.ca/dataset/1d785ef8-f883-47b5-bac5-dce1cdddb1b0/resource/65dd096f-7296-40e8-8cfe-e26b928bcce5/download/remorquages.csv')

    # Clean
    data = data.drop(['SECTEUR_ORIGINE', 'SECTEUR_DESTINATION'], axis=1)
    data.dropna(inplace=True)

    # Rename column: latitude & longitude
    data = data.rename(columns={'LONGITUDE_ORIGINE': 'longitude', 'LATITUDE_ORIGINE': 'latitude'})

    # Transform
    data['date'] = pd.to_datetime(data['DATE_ORIGINE'], format='%Y-%m-%dT%H:%M:%S')
    data['day'] = data['date'].dt.day
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data['hour'] = data['date'].dt.hour
    data['day_of_week'] = data['date'].dt.weekday
    data['day_of_year'] = data['date'].dt.dayofyear
    data['week_of_year'] = data['date'].dt.weekofyear
    data['months'] = data['date'].dt.month_name()
    data['days'] = data['date'].dt.day_name()

    # Data from 2015 is incomplete
    data = data[(data['date'] >= '2016-01-01') & (data['date'] <= data['date'].max())]

    return data

data = load_data()

st.markdown("<br><br>", unsafe_allow_html=True) 

# Year
selected_year = st.selectbox("Year", data.year.unique())
df_year = data[(data.year == selected_year)]
df_y = df_year.groupby(['months']).size().reset_index(name='Number of Occurrences')
chart_altair = alt.Chart(df_y, width= 600, height=100).mark_bar().encode(
       y=alt.X('months', type='nominal', sort=['January', 'February', 'March', "April", "May", "June", "July", "August", "September", "October","November", "December"]),
       x='Number of Occurrences',
    tooltip=['months', 'Number of Occurrences']).interactive()
st.altair_chart(chart_altair)

# Month
selected_month = st.selectbox("Month", ['January', 'February', 'March', "April", "May", "June", "July", "August", "September", "October","November", "December"])

st.markdown("<br>", unsafe_allow_html=True) 

# Day of week
selected_days = st.selectbox("Day of week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
df  = data[(data.year == selected_year) & (data.months == selected_month) & (data.days == selected_days)]


# Select Hour/day
selected_hour = st.slider('Time of the day', 0, 23, 8)

# Line Chart/day
st.write("Total number of towed vehicles on %ss in %s %s" % (selected_days, selected_month, selected_year))

df_hour = df.groupby(['hour']).size().reset_index(name='Number of Occurrences')
chart_altair = alt.Chart(df_hour, width= 600, height=100).mark_line(color='rgb(246,51,102)').encode(
       x=alt.X('hour', type='nominal', sort=None),
       y='Number of Occurrences',
    tooltip=['hour', 'Number of Occurrences']).interactive()
st.altair_chart(chart_altair)



# GeoMap
st.subheader(" between %i:00 and %i:00" % (selected_hour, (selected_hour + 1) % 24))
filtered_data = df[df['date'].dt.hour == selected_hour]

midpoint = (np.average(filtered_data["latitude"]), np.average(filtered_data["longitude"]))
st.deck_gl_chart(
    viewport={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        {
            "type": "HexagonLayer",
            "data": filtered_data,
            "radius": 100,
            "elevationScale": 4,
            "elevationRange": [0, 1000],
            "pickable": True,
            "extruded": True,
        }
    ],
)
# st.map(filtered_data)



# Show Soure
show_source_data = st.checkbox('Show Source')
if show_source_data:
    st.subheader("Source Data")
    st.dataframe(data.head(20))











