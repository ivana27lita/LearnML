import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_palette("Paired")

# Mengakses data yang sudah dibersihkan
url = "https://raw.githubusercontent.com/ivana27lita/kumpulan-dataset/master/clean_bikedata.csv"
day_df = pd.read_csv(url)

# Convert date columns to datetime objects
day_df['date'] = pd.to_datetime(day_df['date'])
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    # Memasukkan logo
    github_image_url = "https://raw.githubusercontent.com/ivana27lita/kumpulan-dataset/master/logo.png"
    st.image(github_image_url, caption='Capital Bike Renting. Co')

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
        help='Pilih rentang waktu'
    )

    # Mengubah start_date dan end_date menjadi objek datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    day_df['date'] = pd.to_datetime(day_df['date'])

    # membuat multiselect untuk kategori hari libur atau bukan
    holiday_categories = st.multiselect('Kategori Hari', day_df['holiday'].unique(), default=day_df['holiday'].unique(), key='holiday_multiselect', help='Pilih kategori hari libur')

    # Menyimpan dataframe yang sudah di filter  
    filtered_df = day_df[(day_df['holiday'].isin(holiday_categories)) & (day_df['date'] >= start_date) & (day_df['date'] <= end_date)]

    # membuat reset filter button
    if st.button("Reset Filters"):
        start_date = min_date
        end_date = max_date
        holiday_categories = day_df['holiday'].unique()
        filtered_df = day_df
        
# membuat header dashboard
st.header('Capital Bike System Dashboard 🚴‍♂️✨')

#Visualisasi 1
st.subheader('Jumlah Casual dan Registered User')

col1, col2 = st.columns(2)
 
with col1:
    # dengan Pie Chart
    fig_pie, ax_pie = plt.subplots(figsize=(4, 4))
    total_casual = filtered_df['casual'].sum()
    total_registered = filtered_df['registered'].sum()
    labels = ['Casual', 'Registered']
    sizes = [total_casual, total_registered]
    ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax_pie.set_title('Persentase Casual dan Registered User')
    st.pyplot(fig_pie)
 
with col2:
    # untuk memberi spasi
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(f"Jumlah Casual User dari {start_date} hingga {end_date}: **{filtered_df['casual'].sum()}**")
    st.write(f"Jumlah Registered User dari {start_date} hingga {end_date}: **{filtered_df['registered'].sum()}**")

# Visualisasi 2
# dengan bar plot
fig2, ax = plt.subplots(figsize=(8, 4))
df_user = pd.melt(filtered_df, id_vars='month', value_vars=['casual', 'registered'])

sns.barplot(x='month', y='value', hue='variable', data=df_user, ax=ax, palette=['blue', 'orange'], ci=None)
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Pengguna')
ax.legend(title='Kategori')
ax.set_title('Jumlah Casual dan Registered User per Bulan')
st.pyplot(fig2)

st.subheader('Jumlah Penyewaan Unit Sepeda')

# Visualisasi 3
# Hitung rata-rata penggunaan sepeda per bulan
monthly_avg = filtered_df.groupby('month')['total_count'].mean().reset_index()

# Temukan indeks bulan dengan rata-rata tertinggi
max_index = monthly_avg['total_count'].idxmax()
max_value = monthly_avg['total_count'][max_index]

# Buat plot
fig3 = plt.figure(figsize=(8, 5))
sns.lineplot(x='month', y='total_count', data=monthly_avg, marker=None, color='blue')

# Tambahkan marker pada nilai tertinggi
plt.scatter(monthly_avg['month'][max_index], max_value, color='red', marker='o', s=100, label='Highest Avg')

# Tambahkan teks nilai pada marker tertinggi
plt.text(monthly_avg['month'][max_index], max_value, f'{max_value:.2f}', color='red', ha='right', va='bottom')

plt.xlabel("Month")
plt.ylabel("Average Bike Usage")
plt.title("Rata-rata Penggunaan Sepeda Per Bulan")
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.legend(loc='upper left')
st.pyplot(fig3)

# Visualisasi 4
fig4 = plt.figure(figsize=(8, 5))

sns.barplot(x='season', y='total_count', hue='weather', data=filtered_df, palette='PuBu',  ci=None)

plt.xlabel("Season")
plt.ylabel("Total Rides")
plt.title("Jumlah Sepeda yang Disewa berdasarkan Cuaca dan Musim")

plt.legend(title='Weather', loc='upper left')

st.pyplot(fig4)

# Visualisasi 5
fig5 = plt.figure(figsize=(8,5))

sns.barplot(x='month', y='total_count', hue='year', data=filtered_df, palette='Paired',  ci=None)

sns.lineplot(x='month', y='total_count', hue='year', data=filtered_df, linestyle='solid',  ci=None, markers=True)

plt.xlabel("Month")
plt.ylabel("Total Rides")
plt.title("Total Bike Sharing Per Bulan")
plt.legend(title='Year', loc='upper left')

st.pyplot(fig5)
