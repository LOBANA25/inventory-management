from flask import Blueprint, render_template, request, redirect, url_for, make_response
from . import db
from .models import Product, Location, ProductMovement


bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

# Product Views
@bp.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('product.html', products=products)

@bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        product = Product(product_id=product_id, name=name)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('routes.view_products'))
    return render_template('add_edit_product.html')

@bp.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        db.session.commit()
        return redirect(url_for('routes.view_products'))
    return render_template('add_edit_product.html', product=product)

# Location Views
@bp.route('/locations')
def view_locations():
    locations = Location.query.all()
    return render_template('location.html', locations=locations)

@bp.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        name = request.form['name']
        location = Location(location_id=location_id, name=name)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('routes.view_locations'))
    return render_template('add_edit_location.html')

@bp.route('/edit_location/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get(location_id)
    if request.method == 'POST':
        location.name = request.form['name']
        db.session.commit()
        return redirect(url_for('routes.view_locations'))
    return render_template('add_edit_location.html', location=location)

# Movement Views
@bp.route('/movements')
def view_movements():
    movements = ProductMovement.query.all()
    return render_template('movement.html', movements=movements)

@bp.route('/add_movement', methods=['GET', 'POST'])
def add_movement():
    if request.method == 'POST':
        movement_id = request.form['movement_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']
        movement = ProductMovement(movement_id=movement_id, from_location=from_location, to_location=to_location, product_id=product_id, qty=qty)
        db.session.add(movement)
        db.session.commit()
        return redirect(url_for('routes.view_movements'))
    return render_template('add_movement.html')

# Report View
@bp.route('/report')
def report():
    report_data = db.session.query(
        Product.product_id, Product.name, Location.location_id, Location.name, db.func.sum(ProductMovement.qty).label('total_qty')
    ).join(ProductMovement, Product.product_id == ProductMovement.product_id
    ).join(Location, Location.location_id == ProductMovement.to_location
    ).group_by(Product.product_id, Location.location_id).all()
    
    return render_template('report.html', report_data=report_data)

def generate_report(report_data):
    html = "<table border='1'><tr><th>Name</th><th>Age</th><th>City</th></tr>"
    for row in report_data:
        html += "<tr>"
        for key, value in row.items():
            html += f"<td>{value}</td>"
        html += "</tr>"
    html += "</table>"
    return html
@bp.route('/download')
def download_report():
    report_data=report()
    report_content = generate_report(report_data)
    response = make_response(report_content)
    response.headers["Content-Disposition"] = "attachment; filename=report.html"
    response.headers["Content-Type"] = "text/html"
    return response