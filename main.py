import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('C:/Users/Dell/Desktop/Deployment/Sales_Data.csv')
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, dayfirst=True, errors='coerce')
df['Month'] = df['Date'].dt.strftime('%b')
df['Amount'] = df['Amount'].str.replace(',', '').astype(float).astype(int)
df['Price'] = df['Price'].str.replace(',', '').astype(float).astype(int)

# Set page configuration
st.set_page_config(
    page_title="Electronics Dashboard Report",
    page_icon=":bar_chart:",
    layout="wide"
)

# Sidebar
sidebar_menu = st.sidebar.selectbox("Navigation", ["Main", "Data", "Data Analysis", "Conclusion"])

# Main section
if sidebar_menu == "Main":
    st.title(":bar_chart: Electronics Dashboard Report")
    st.markdown("##")
    st.write("""
    Here is the sales data of a particular company that sells electronic Gadgets in different cities of India.
    We have the records from the first week of January 2021 to the last week of December 2021. Our objectives are:
   \n (1) Amount of Sales done by each Sales Representative
    \n(2) Amount of Productwise sales in each month of the year 2021
    \n(3) Amount of sales happened in monthwise of the year 2021
    \n(4) Amount of Sales by category
    \n(5) Amount of Product sold on a particular day
    """)
    st.divider()

# Data section
elif sidebar_menu == "Data":
    st.markdown("## Data Introduction ")
    st.write(""" The dataset contain 
    dates are in the First Column product 
    name in the second column category in 
    the third column name of sales 
    representative in the fourth column name 
    of city in the fifth column number of 
    units sold in the sixth column unit price 
    and amount in the third and second  last column & so on ... There dataset contains 1559 rows and 9 columns""")
    
    # Display data table
    st.write("### Sales Data Table")
    st.dataframe(df)

# Data Analysis section
elif sidebar_menu == "Data Analysis":
    st.markdown("## Data Analysis ")
    st.sidebar.header("Choose your filter:")

    # Sidebar filters
    months_list = df['Month'].dropna().unique()
    months_list.sort()  # Sorting the list
    selected_month = st.sidebar.multiselect(
        "Pick the Month:",
        options=months_list,
        default=months_list
    )

    selected_product = st.sidebar.multiselect(
        "Pick the Product:",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    selected_category = st.sidebar.multiselect(
        "Pick the category:",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    selected_sales_rep = st.sidebar.multiselect(
        "Pick the Sales_Rep:",
        options=df["Sales Rep"].unique(),
        default=df["Sales Rep"].unique()
    )

    # Filter data based on user selection
    filtered_data = df[df['Month'].isin(selected_month) & df['Product'].isin(selected_product) &
                    df['Category'].isin(selected_category) & df['Sales Rep'].isin(selected_sales_rep)]

    # Modify the 'Date' column to remove the time portion
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')

    # Organize the layout using rows and columns
    col1, col2 = st.columns([1, 1])

    with col1:
        # Sales by salesRep (bar chart)
        sales_Rep = filtered_data.groupby(['Sales Rep'])['Amount'].sum().reset_index()
        sales_by_salesRep = px.bar(sales_Rep, x="Amount", y="Sales Rep", orientation="h", title="Sales by SalesRep")
        st.plotly_chart(sales_by_salesRep)

        # Monthwise sales (bar chart)
        Monthly_sales = filtered_data.groupby(['Month'])['Amount'].sum().reset_index()
        Monthwise_sales = px.bar(Monthly_sales, x='Amount', y='Month', orientation="h", title='Monthwise Sales')
        st.plotly_chart(Monthwise_sales)

    with col2:
        # Productwise sales (bar chart)
        sales_by_productwise = filtered_data.groupby(by=["Product"])["Amount"].sum().reset_index()
        productwise_sale = px.bar(sales_by_productwise, x="Amount", y="Product", orientation="h", title="Productwise Sales")
        st.plotly_chart(productwise_sale)

        # Sales by category (pie chart)
        category_data = filtered_data.groupby(['Category'])['Amount'].sum().reset_index()
        by_category = px.pie(category_data, values='Amount', names='Category', title='Category by Sales')
        st.plotly_chart(by_category)

    # 3D Scatter plot
    scatter_3d = px.scatter_3d(
        filtered_data,
        x='Date',
        y='Product',
        z='Amount',
        color='Amount',
        size='Amount',
        title='3D Scatter Plot - Date vs Product vs Amount'
    )
    st.plotly_chart(scatter_3d)

# Conclusion section
elif sidebar_menu == "Conclusion":
    st.markdown("## Conclusion ")
    st.write(""" from the analysis, we conclude
 that the bar chart gives the Amount of Sales done by each Sales Representative,
    Amount of Productwise sales in each month of the year 2021, Amount of sales happened in monthwise of the year 2021
    and pie chart gives Amount of Sales by category and 3D scatter plot gives Amount of Product sold on a particular day. 
    so our objective is fulfilled.""")

