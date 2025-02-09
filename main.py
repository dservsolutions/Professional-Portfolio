from crypt import methods
from xml.sax.handler import property_interning_dict

from flask import render_template, Flask, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm.sync import update
from werkzeug.utils import redirect

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SECRET_KEY'] = "ZJ\x9e\xc74N\x8d\xe5\xe8\x05\xd2w\xab\xbe\\\xe2+\x01\xac\x9c\x94\xa7\xfbc"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CAFE Table Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)

    #
    def __repr__(self):
        return '<Name %r>' % self.name


with app.app_context():
    db.create_all()


def index_card():
    query = db.session.execute(db.select(Cafe))
    result = query.scalars().all()
    items = [data for data in result]
    return items, result


@app.route('/')
def home():
    items = index_card()
    item_1 = items[0]
    item_2 = items[1]
    return render_template('index.html', first_card=item_1, second_card=item_2)


@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        data = request.form
        toilet = 'toilet' in request.form
        wifi = 'wifi' in request.form
        sockets = 'sockets' in request.form
        calls = 'calls' in request.form
        new_cafe = Cafe(
            name=data.get('name'),
            map_url=data.get('map_url'),
            img_url=data.get('img_url'),
            location=data.get('location'),
            seats=data.get('seats'),
            coffee_price=data.get('coffee_price'),
            has_toilet=toilet,
            has_wifi=wifi,
            has_sockets=sockets,
            can_take_calls=calls
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash("Save Success")
        return redirect(url_for('all_places'))
    return render_template('add.html')


@app.route('/all_places')
def all_places():
    query = db.session.execute(db.select(Cafe))
    result = query.scalars().all()
    return render_template('all_places.html', places=result)

@app.route('/edit', methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        cafe_id = request.form['id']
        has_toilet = 'has_toilet' in request.form
        has_wifi = 'has_wifi' in request.form
        has_sockets = 'has_sockets' in request.form
        can_take_calls = 'can_take_calls' in request.form
        cafe_to_update = db.get_or_404(Cafe, cafe_id)
        cafe_to_update.name = request.form['name']
        cafe_to_update.map_url = request.form['map_url']
        cafe_to_update.img_url = request.form['img_url']
        cafe_to_update.location = request.form['location']
        cafe_to_update.seats = request.form['seats']
        cafe_to_update.coffee_price = request.form['coffee_price']
        cafe_to_update.has_toilet = has_toilet
        cafe_to_update.has_wifi = has_wifi
        cafe_to_update.has_sockets = has_sockets
        cafe_to_update.can_take_calls = can_take_calls
        db.session.commit()
        return redirect(url_for('all_places'))
    cafe_id = request.args.get('id')
    cafe_selected = db.get_or_404(Cafe, cafe_id)
    return render_template('edit.html' ,cafe=cafe_selected)

@app.route('/delete')
def delete():
    cafe_id = request.args.get('id')
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('all_places'))




if __name__ == "__main__":
    app.run(debug=True, port=5001)
