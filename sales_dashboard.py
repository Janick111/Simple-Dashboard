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
df['YearQuarter'] = df['Year'].astype(str) + 'Q' + (df['Month'].apply(lambda x: (pd.to_datetime(x, format='%b').month - 1) // 3 + 1)).astype(str)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    view = request.form.get('view', 'monthly')  # Default to 'monthly'
    category = request.form.get('category', 'All')  # Default to 'All' categories

    # Filter by category
    if category != 'All':
        df_filtered = df[df['Category'] == category]
    else:
        df_filtered = df.copy()

    total_sales = df_filtered['Sales'].sum()
    average_sales = df_filtered['Sales'].mean()
    max_sales = df_filtered['Sales'].max()
    min_sales = df_filtered['Sales'].min()

    categories = df['Category'].unique().tolist()

    if view == 'yearly':
        df_grouped = df_filtered.groupby(['Year', 'Category'], as_index=False)['Sales'].sum()
        x_axis = 'Year'
        title = 'Yearly Sales by Category'
    elif view == 'quarterly':
        df_grouped = df_filtered.groupby(['YearQuarter', 'Category'], as_index=False)['Sales'].sum()
        x_axis = 'YearQuarter'
        title = 'Quarterly Sales by Category'
    else:
        df_grouped = df_filtered.groupby(['Date', 'Category'], as_index=False)['Sales'].sum()
        x_axis = 'Date'
        title = 'Monthly Sales by Category'

    bar_fig = px.bar(df_grouped, x=x_axis, y='Sales', color='Category', title=f'{title}',
                     labels={'Sales': 'Sales (€)'}, template='plotly_white')
    line_fig = px.line(df_grouped, x=x_axis, y='Sales', color='Category', title=f'{title} Trend',
                       labels={'Sales': 'Sales (€)'}, template='plotly_white')

    bar_fig.update_layout(showlegend=True, xaxis_title=x_axis)
    line_fig.update_layout(showlegend=True, xaxis_title=x_axis)

    bar_graph_html = bar_fig.to_html(full_html=False)
    line_graph_html = line_fig.to_html(full_html=False)

    return render_template('index.html', bar_graph_html=bar_graph_html, line_graph_html=line_graph_html, view=view,
                           total_sales=total_sales, average_sales=average_sales, max_sales=max_sales, min_sales=min_sales,
                           categories=categories, category=category)

if __name__ == '__main__':
    app.run(debug=True)