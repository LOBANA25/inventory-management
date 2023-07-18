from flask import Flask,render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///pro1.db'
db=SQLAlchemy(app)

class Product(db.Model):
    id=db.Column(db.VARCHAR(200),primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    qty=db.Column(db.Integer,nullable=False)


class Location(db.Model):
    id=db.Column(db.VARCHAR(200),primary_key=True)
    names=db.Column(db.String(200),nullable=False)


class product_movement(db.Model):
    id = db.Column(db.VARCHAR(200), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    qty = db.Column(db.Integer, nullable=False)

    def from_location_name(self):
        return location.query.get(self.from_location_id).name if self.from_location_id else ''

    def to_location_name(self):
        return location.query.get(self.to_location_id).name if self.to_location_id else ''
    

@app.route('/')
def base():
    products = Product.query.all()
    return render_template('base.html',products=products)

@app.route('/product/<string:id>/edit', methods=['GET', 'POST'])
def product_edit(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('product.html', product=product)


@app.route('/product/add', methods=['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        qty=request.form['qty']
        product = Product(id=id,name=name,qty=qty)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product_add'))
    return render_template('product.html')

@app.route('/product')
def product_view():
    products = Product.query.all()
    return render_template('product.html', products=products)


@app.route('/location/add', methods=['GET', 'POST'])
def location_add():
    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        loc= Location(id=id,name=name)
        db.session.add(loc)
        db.session.commit()
        return redirect(url_for('location'))
    return render_template('location.html')

def product_movement():
    product = request.form['product']
    source = request.form['source']
    destination = request.form['destination']
@app.route('/location')
def location():
    return render_template('location.html')


@app.route('/movement')
def movement():
    return render_template('movement.html')

@app.route('/report')
def report():
    return render_template('report.html')
@app.route('/home')
def home():
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)
