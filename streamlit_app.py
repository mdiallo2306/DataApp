import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
##option = st.selectbox("Select a Category:", ("Furniture", "Office Supplies", "Technology"))
option = st.selectbox("Select a category:", df["Category"].unique())
filtered_df = df[df["Category"] == option]
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
sub_categories = st.multiselect("Select a sub category: ", filtered_df["Sub_Category"].unique())


# Define sub-categories for each category
#sub_categories = {
 #   "Furniture": ["Chairs", "Tables", "Bookcases"],
  #  "Office Supplies": ["Pens", "Paper", "Binders"],
   # "Technology": ["Computers", "Printers", "Phones"]
#}

# Create a multi-select for sub-categories based on selected category
#if option:
 #   sub_category_options = st.multiselect(
  #      "Select a sub category:", sub_categories[option]
   # )

st.write("### (3) show a line chart of sales for the selected items in (2)")
selected_df = filtered_df[filtered_df["Sub_Category"].isin(sub_categories)]
if not selected_df.empty:
    sales_by_date = selected_df.groupby('Order_Date')['Sales'].sum().reset_index()
    st.line_chart(sales_by_date.set_index('Order_Date'), y="Sales")
else:
    st.write("No data available for the selected subcategories.")

# Calculate the overall profit margin for all products
total_sales_all = df['Sales'].sum()
total_profit_all = df['Profit'].sum()
overall_profit_margin = (total_profit_all / total_sales_all) * 100 if total_sales_all != 0 else 0

if not selected_df.empty:
    total_sales = selected_df['Sales'].sum()
    total_profit = selected_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    profit_margin_delta = profit_margin - overall_profit_margin

    st.write("### (4 + 5) Metrics for the Selected Items (including Delta change)")
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
else:
    st.write("Metrics are not available due to no data in the selected subcategories.")

#st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")



