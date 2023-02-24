from flask import Flask, render_template, request, redirect
from cloudipsp import Api, Checkout
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    isActive = db.Column(db.Boolean, default=True)



@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create-lot', methods=['POST', 'GET'])
def create():
    if request.method=='POST':
        title = request.form['title']
        price = request.form['price']

        data = Item(title=title, price=price)

        try:
            db.session.add(data)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"

    else:
        return render_template('create-lot.html')

@app.route('/buy/<int:id>')
def lot_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)




if __name__ == '__main__':
    app.run(debug=True)