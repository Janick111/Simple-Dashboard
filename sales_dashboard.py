from flask import Flask, render_template
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Sample sales data (mimics CSV input)
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Sales': [1200, 1500, 1300, 1700, 1600, 1800, 2000, 1900, 2100, 2200, 2000, 2300]
}
df = pd.DataFrame(data)

@app.route('/')
def dashboard():
    # Create bar chart using Plotly
    fig = px.bar(df, x='Month', y='Sales', title='Monthly Sales for Retail Shop',
                 labels={'Sales': 'Sales (€)'}, template='plotly_white')
    fig.update_layout(showlegend=False)
    graph_html = fig.to_html(full_html=False)
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)