from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import plotly.express as px
import pandas as pd

app = Flask(__name__)
Bootstrap(app)

# Read data from CSV file
df = pd.read_csv('sales_data.csv')

# Create a datetime column for proper ordering
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b')

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    view = request.form.get('view', 'monthly')  # Default to 'monthly'

    total_sales = df['Sales'].sum()
    average_sales = df['Sales'].mean()
    max_sales = df['Sales'].max()
    min_sales = df['Sales'].min()

    if view == 'yearly':
        df_yearly = df.groupby('Year', as_index=False)['Sales'].sum()
        bar_fig = px.bar(df_yearly, x='Year', y='Sales', title='Yearly Sales for Retail Shop',
                         labels={'Sales': 'Sales (€)'}, template='plotly_white')
        line_fig = px.line(df_yearly, x='Year', y='Sales', title='Yearly Sales Trend',
                           labels={'Sales': 'Sales (€)'}, template='plotly_white')
    else:
        bar_fig = px.bar(df, x='Date', y='Sales', title='Monthly Sales for Retail Shop',
                         labels={'Sales': 'Sales (€)'}, template='plotly_white')
        line_fig = px.line(df, x='Date', y='Sales', title='Monthly Sales Trend',
                           labels={'Sales': 'Sales (€)'}, template='plotly_white')

    bar_fig.update_layout(showlegend=True, xaxis_title='Year')
    line_fig.update_layout(showlegend=True, xaxis_title='Year')

    bar_graph_html = bar_fig.to_html(full_html=False)
    line_graph_html = line_fig.to_html(full_html=False)

    return render_template('index.html', bar_graph_html=bar_graph_html, line_graph_html=line_graph_html, view=view,
                           total_sales=total_sales, average_sales=average_sales, max_sales=max_sales, min_sales=min_sales)

if __name__ == '__main__':
    app.run(debug=True)