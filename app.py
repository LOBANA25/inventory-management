from flask import Flask,render_template,request, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///projects.db'
db=SQLAlchemy(app)

class Product(db.Model):
    product_id=db.Column(db.VARCHAR(200),primary_key=True)
    product_name=db.Column(db.String(200),nullable=False)
    qty=db.Column(db.Integer,nullable=False)


class Location(db.Model):
    location_id=db.Column(db.VARCHAR(200),primary_key=True)
    location_names=db.Column(db.String(200),nullable=False)


class product_movement(db.Model):
    mov_id = db.Column(db.VARCHAR(200), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer, nullable=False)

    def from_location_name(self):
        return location.query.get(self.from_location_id).name if self.from_location_id else ''

    def to_location_name(self):
        return location.query.get(self.to_location_id).name if self.to_location_id else ''
    

@app.route('/')
def base():
    products = Product.query.all()
    return render_template('base.html',products=products)
'''
@app.route('/update_product_form/<string:id>', methods=['GET'])
def update_product_form(id):
    return render_template('update_product.html', id=id)
'''


'''
@app.route('/product/<string:id>/edit', methods=['GET', 'POST'])
def product_edit(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('product.html', product=product)
'''

@app.route('/product/add', methods=['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        product_id=request.form['id']
        product_name = request.form['name']
        qty=request.form['qty']
        product = Product(product_id=product_id,product_name=product_name,qty=qty)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product_add'))
    return render_template('product.html')

@app.route('/product/<string:id>', methods=['POST'])
def update_product(id):
    movement = Product.query.get(id)
    #print(movement)
    if movement:
        if 'Update' in request.form:
            new_qty = request.form.get('qty')
            if new_qty:
                movement.qty = new_qty
                db.session.commit()
                return redirect(url_for('update_product',id=id))
            else:
                return render_template('product.html')
        elif 'Delete' in request.form:
            db.session.delete(movement)
            db.session.commit()
            return redirect(url_for('update_product',id=id))
        else:
            return render_template('product.html')
    else:
        return render_template('product.html')

@app.route('/product')
def product_view():
    products = Product.query.all()
    return render_template('product.html', products=products)

@app.route('/productmovement/add', methods=['GET', 'POST'])
def add_product_movement():
    if request.method == 'POST':
        # Retrieve form data
        mov_id = request.form['mov_id']
        timestamp = request.form['timestamp']
        from_location_id = request.form['from_location']
        to_location_id = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']
        
        product_movement =product_movement(mov_id=mov_id, timestamp=timestamp,
                                           from_location_id=from_location_id, to_location_id=to_location_id,
                                           product_id=product_id, qty=qty)
        
        db.session.add(product_movement)
        db.session.commit()
        
        return redirect('/productmovement')
    else:
        return render_template('movement.html')


@app.route('/productmovement/edit/<movement_id>', methods=['GET', 'POST'])
def edit_product_movement(movement_id):
    product_movement = product_movement.query.get(movement_id)
    
    if request.method == 'POST':
        # Retrieve form data
        product_movement.timestamp = request.form['timestamp']
        product_movement.from_location = request.form['from_location']
        product_movement.to_location = request.form['to_location']
        product_movement.product_id = request.form['product_id']
        product_movement.qty = request.form['qty']
        
        # Update the ProductMovement instance in the database
        db.session.commit()
        
        return redirect('/productmovement')
    else:
        return render_template('movement.html', product_movement=product_movement)


@app.route('/productmovement')
def movement():
    product_movements = product_movement.query.all()
    return render_template('movement.html')


@app.route('/location/add', methods=['GET', 'POST'])
def location_add():
    if request.method == 'POST':
        location_id=request.form['id']
        location_names = request.form['name']
        loc= Location(location_id=location_id,location_names=location_names)
        db.session.add(loc)
        db.session.commit()
        return redirect(url_for('location'))
    return render_template('location.html')

@app.route('/location')
def location():
    locations = Location.query.all()
    return render_template('location.html',locations=locations)




@app.route('/report')
def report():
    return render_template('report.html')
@app.route('/home')
def home():
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)
