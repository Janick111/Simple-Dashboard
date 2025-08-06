from flask import Blueprint, render_template, request, redirect, url_for, current_app
import pandas as pd

sales_data_bp = Blueprint('sales_data', __name__)

@sales_data_bp.route('/add-sales', methods=['GET', 'POST'])
def add_sales():
    app = current_app

    # --- Sorting logic ---
    order_by = request.args.get('order_by', 'Date')
    order_dir = request.args.get('order_dir', 'desc')
    ascending = order_dir == 'asc'

    df = app.df.copy()
    if order_by in df.columns:
        df = df.sort_values(by=order_by, ascending=ascending)
    else:
        df = df.sort_values(by='Date', ascending=False)

    categories = df['Category'].unique().tolist()
    sales_data = df[['Year', 'Month', 'Sales', 'Category']].reset_index()  # Include index

    return render_template(
        'sales_data_form.html',
        categories=categories,
        sales_data=sales_data,
        order_by=order_by,
        order_dir=order_dir
    )

@sales_data_bp.route('/edit-sales/<int:index>', methods=['GET', 'POST'])
def edit_sales(index):
    app = current_app
    if index not in app.df.index:
        return "Record not found", 404

    row = app.df.loc[index]

    if request.method == 'POST':
        app.df.at[index, 'Year'] = int(request.form.get('year'))
        app.df.at[index, 'Month'] = request.form.get('month')
        app.df.at[index, 'Sales'] = float(request.form.get('sales'))
        app.df.at[index, 'Category'] = request.form.get('category')
        app.df.to_csv('sales_data.csv', index=False)
        return redirect(url_for('sales_data.add_sales'))

    categories = app.df['Category'].unique().tolist()
    sales_data = pd.DataFrame([row])  # Pass as DataFrame for consistency
    return render_template(
        'sales_data_form.html',  # Reuse the same template
        categories=categories,
        sales_data=sales_data,
        index=index,
        is_edit=True  # Flag to indicate edit mode
    )

@sales_data_bp.route('/delete-sales/<int:index>', methods=['GET'])
def delete_sales(index):
    app = current_app
    if index in app.df.index:
        app.df = app.df.drop(index).reset_index(drop=True)
        app.df.to_csv('sales_data.csv', index=False)
    return redirect(url_for('sales_data.add_sales'))