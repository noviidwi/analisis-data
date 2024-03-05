import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')
colors = ['#72BCD4', '#D3D3D3']


def load_data():
    df = pd.read_csv("../main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['day_type'] = df['dteday'].dt.dayofweek.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    return df

# Load and preprocess the data
df = load_data()

# Sidebar - Date filter
with st.sidebar:
    # Logo
    st.image("logo.png")
    
    # Date input for filtering
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=df['dteday'].min().date(),
        max_value=df['dteday'].max().date(),
        value=[df['dteday'].min().date(), df['dteday'].max().date()]
    )

# Filter the dataframe based on the selected date range
filtered_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

# Main dashboard header
st.title('Dashboard Penyewaan Sepeda')

# Display bar chart for bike rentals by day type in a single column
st.header('Jumlah penyewaan sepeda antara hari kerja dan akhir pekan')
day_type_counts = filtered_df.groupby('day_type')['cnt'].sum()

# Create bar plot using matplotlib with adjusted y-axis range
fig, ax = plt.subplots(figsize=(8, 4))

day_type_counts.plot(kind='bar', color=colors, ax=ax)
plt.xlabel('Day Type')
plt.ylabel('Total Bike Rentals')
plt.title('Total Bike Rentals by Day Type')

# Adjust y-axis range
ax.set_ylim(0, 1.2 * max(day_type_counts))

st.pyplot(fig)

# Calculate and display table for total bike rentals by day type
st.header('Total Penyewa Sepeda di Hari Kerja dan Akhir Pekan')
total_rentals_by_day_type = filtered_df.groupby('day_type')['cnt'].sum().reset_index()
total_rentals_by_day_type.columns = ['Tipe Hari', 'Jumlah Penyewa']
st.table(total_rentals_by_day_type)

# Display line chart for bike rentals by hour in full width
st.header('Jam penyewaan sepeda selama hari kerja dibandingkan akhir pekan')
hourly_counts = df.groupby(['hr', 'day_type'])['cnt'].mean().unstack()
fig, ax = plt.subplots(figsize=(12, 6))

for day_type in hourly_counts.columns:
    ax.plot(hourly_counts.index, hourly_counts[day_type], marker='o', label=day_type, color=colors[hourly_counts.columns.get_loc(day_type)])

ax.set_title('Average Bike Rentals by Hour')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Number of Rentals')
ax.legend()

plt.xticks(hourly_counts.index)
st.pyplot(fig)

# Display table for busiest hours
st.header('Jam paling sering disewa selama hari kerja dibandingkan akhir pekan')
busiest_hours = pd.DataFrame(hourly_counts.idxmax())
busiest_hours.columns = ['Tipe Hari']
busiest_hours.index.name = 'Jam'
busiest_hours.columns.name = None
busiest_hours.reset_index(inplace=True)
st.table(busiest_hours)

# Footer
st.caption('Dicoding | Novi Dwi Fitriani - Machine Learning [60]')