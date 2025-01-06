import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#sns.set(style='dark')
all_df = pd.read_csv("all_data.csv")
#set datetime type columns
datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
for column in datetime_columns:
   all_df[column] = pd.to_datetime(all_df[column])

def create_delivered_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "payment_amount"
    }, inplace=True)
    
    return daily_orders_df

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

st.header(':sparkles: Tugas Analisis Data Dashboard :sparkles:')

st.subheader('Delivered Daily Orders')
delivered_daily_orders_df = create_delivered_daily_orders_df(main_df)

col1, col2 = st.columns(2)
 
with col1:
    total_orders = delivered_daily_orders_df.order_count.sum()
    st.metric("Total delivered orders", value=total_orders)
 
with col2:
    total_payment = format_currency(delivered_daily_orders_df.payment_amount.sum(), "$ ", locale='es_CO') 
    st.metric("Total Payment", value=total_payment)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    delivered_daily_orders_df["order_purchase_timestamp"],
    delivered_daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Most Customer's City")
customers_group_by_city_df = main_df[['customer_id','customer_city']].groupby('customer_city')['customer_city'].count().reset_index(name='total_customer').sort_values(['total_customer'], ascending=False)

plt.figure(figsize=(12,5))
colors = ["#00ac4e", "#acd1af", "#acd1af", "#acd1af", "#acd1af", "#acd1af", "#acd1af", "#acd1af", "#acd1af", "#acd1af"]

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
ax = sns.barplot(data=customers_group_by_city_df.head(10), x="total_customer", y="customer_city", hue='customer_city', palette=colors)
for i in range(10):
    ax.bar_label(ax.containers[i], padding=2, fontsize=10)

plt.title("City With The Most Customers", loc="center", fontsize=15)
plt.ylabel("City", fontsize=15)
plt.xlabel("Total Customer", fontsize=15)
plt.tick_params(axis='y', labelsize=12)
plt.show()

st.pyplot(plt)

st.subheader("Percentage Value for Each Payment Type")
value_group_by_payment_type_df = main_df.groupby('payment_type')['payment_value'].sum().reset_index(name='payment_value').sort_values(['payment_value'], ascending=False)
total_payment_value = main_df['payment_value'].sum()
value_group_by_payment_type_df['percentage'] = round(((value_group_by_payment_type_df['payment_value'] / total_payment_value) * 100),2)

plt2.figure(figsize=(8,7))
colors = ["#acd1af", "#FBE29F", "#9BBFE0", "#F13C59"]

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
ax = sns.barplot(data=value_group_by_payment_type_df, x="payment_type", y="percentage", hue='payment_value', palette=colors)

plt2.title("Persentase value dari setiap tipe pembayaran", loc="center", fontsize=15)


plt2.ylabel("% Usage", fontsize=10)
plt2.xlabel("Payment Type", fontsize=10)
for i in range(4):
    ax.bar_label(ax.containers[i], fmt='%.2f%%', padding=2, fontsize=10)
plt2.show()
st.pyplot(plt2)