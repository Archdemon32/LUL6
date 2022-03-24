import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

githubpath = './data/'
df_customers = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="customers")
df_order = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="order")
df_employee = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="employee")
df_products = pd.read_excel(githubpath + 'my_shop_data.xlsx', sheet_name="products")

def get_data():
    df_employee['Employee_Names'] = df_employee['firstname'] + ' ' + df_employee['lastname']
    df_order['Sales'] = df_order['unitprice'] * df_order['quantity']

    order = pd.merge(df_order, df_products, on='product_id')
    order = pd.merge(order, df_employee, on='employee_id')
    order = pd.merge(order, df_customers, on='customer_id')

    return order

order = get_data()

# fig_product=px.bar(order,
#     x='productname', y='Sales',
#     color='type', title='Sales by product',
#     labels={'Sales':'Total Sales', 'productname':'Products', 'type':'Product Type'})

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Sales by Employees'),
    dcc.Graph(id="graph"),])

@app.callback(
    Output("graph", "figure"))
def update_bar_chart(day):
    mask = df["type"] == type
    fig_employee = px.bar(order,
        x='Employee_Names', y='Sales',
        color='type', title='Sales by Employee',
        labels={'Sales':'Total Sales', 'Employee_Names':'Employee', 'type':'Product Type'})
    return fig

app.run_server(debug=True)
