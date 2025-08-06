from flask import Flask
from flask_bootstrap import Bootstrap
import pandas as pd

from py.dashboard import dashboard_bp
from py.sales_data import sales_data_bp

app = Flask(__name__)
Bootstrap(app)

# Load DataFrame and attach to app
app.df = pd.read_csv('sales_data.csv')
app.df['Date'] = pd.to_datetime(
    app.df['Year'].astype(str) + '-' + app.df['Month'],
    format='%Y-%b'
)
app.df['YearQuarter'] = (
    app.df['Year'].astype(str)
    + 'Q'
    + (
        app.df['Month'].apply(
            lambda x: (pd.to_datetime(x, format='%b').month - 1) // 3 + 1
        )
    ).astype(str)
)

# Register blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(sales_data_bp)

if __name__ == "__main__":
    app.run(debug=True)