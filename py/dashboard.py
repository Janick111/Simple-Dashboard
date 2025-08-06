from flask import Blueprint, render_template, request, redirect, url_for, current_app
import plotly.express as px
import pandas as pd

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET', 'POST'])
def dashboard():
    app = current_app
    view = request.form.get('view', 'monthly')
    category = request.form.get('category', 'All')
    df_filtered = app.df if category == 'All' else app.df[app.df['Category'] == category]
    stats = {
        "total_sales": df_filtered['Sales'].sum(),
        "average_sales": df_filtered['Sales'].mean(),
        "max_sales": df_filtered['Sales'].max(),
        "min_sales": df_filtered['Sales'].min(),
    }
    categories_info = {
        "all_categories": app.df['Category'].unique().tolist(),
        "selected": category
    }
    groupings = {
        'yearly': {
            'df': df_filtered.groupby(['Year', 'Category'], as_index=False)['Sales'].sum(),
            'x_axis': 'Year',
            'title': 'Yearly Sales by Category'
        },
        'quarterly': {
            'df': df_filtered.groupby(['YearQuarter', 'Category'], as_index=False)['Sales'].sum(),
            'x_axis': 'YearQuarter',
            'title': 'Quarterly Sales by Category'
        },
        'monthly': {
            'df': df_filtered.groupby(['Date', 'Category'], as_index=False)['Sales'].sum(),
            'x_axis': 'Date',
            'title': 'Monthly Sales by Category'
        }
    }
    grouping = groupings.get(view, groupings['monthly'])
    x_axis = grouping['x_axis']
    title = grouping['title']
    figures = {
        'bar': px.bar(grouping['df'], x=x_axis, y='Sales', color='Category', title=title,
                      labels={'Sales': 'Sales (€)'}, template='plotly_white'),
        'line': px.line(grouping['df'], x=x_axis, y='Sales', color='Category',
                        title=f'{title} Trend',
                        labels={'Sales': 'Sales (€)'},
                        template='plotly_white')
    }
    figures['bar'].update_layout(showlegend=True, xaxis_title=x_axis)
    figures['line'].update_layout(showlegend=True, xaxis_title=x_axis)
    graphs = {
        'bar_graph_html': figures['bar'].to_html(full_html=False),
        'line_graph_html': figures['line'].to_html(full_html=False)
    }
    return render_template(
        'index.html',
        graphs=graphs,
        view=view,
        stats=stats,
        categories_info=categories_info
    )