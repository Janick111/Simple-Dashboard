from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Sample sales data for 5 years with different sales values for each year
data = {
    'Year': [2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019, 2019,
             2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020, 2020,
             2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021, 2021,
             2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022,
             2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023],
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] * 5,
    'Sales': [
        1200, 1500, 1300, 1700, 1600, 1800, 2000, 1900, 2100, 2200, 2000, 2300,  # 2019
        1300, 1600, 1400, 1800, 1700, 1900, 2100, 2000, 2200, 2300, 2100, 2400,  # 2020
        1400, 1700, 1500, 1900, 1800, 2000, 2200, 2100, 2300, 2400, 2200, 2500,  # 2021
        1500, 1800, 1600, 2000, 1900, 2100, 2300, 2200, 2400, 2500, 2300, 2600,  # 2022
        1600, 1900, 1700, 2100, 2000, 2200, 2400, 2300, 2500, 2600, 2400, 2700   # 2023
    ]
}
df = pd.DataFrame(data)

# Create a datetime column for proper ordering
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b')

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # Get filter option from request
    view = request.form.get('view', 'monthly')  # Default to 'monthly'

    # Calculate total, average, max, and min sales
    total_sales = df['Sales'].sum()
    average_sales = df['Sales'].mean()
    max_sales = df['Sales'].max()
    min_sales = df['Sales'].min()

    if view == 'yearly':
        # Aggregate data by year, summing only the 'Sales' column
        df_yearly = df.groupby('Year', as_index=False)['Sales'].sum()
        bar_fig = px.bar(df_yearly, x='Year', y='Sales', title='Yearly Sales for Retail Shop',
                         labels={'Sales': 'Sales (€)'}, template='plotly_white')
        line_fig = px.line(df_yearly, x='Year', y='Sales', title='Yearly Sales Trend',
                           labels={'Sales': 'Sales (€)'}, template='plotly_white')
    else:
        # Use monthly data with continuous date
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