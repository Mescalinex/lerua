from flask import Flask, render_template
from tools.parse import parseHandler
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    link = db.Column(db.String(120))
    category = db.Column(db.String(120))

    def __repr__(self):
        return '{} {}'.format(self.id, self.title)


@app.route('/loadData')
def loadData():
    db.drop_all()
    db.create_all()
    catalogue = parseHandler('https://leroymerlin.ru/catalogue/', 'div.items li', 'a span', 'a')

    for subCat in catalogue[0:5]:
        subCatList =  parseHandler(subCat['link'], 'div.items li', 'a span', 'a')

    for good in subCatList[0:5]:
        goodList = parseHandler(good['link'], 'div.items li', 'a span', 'a')

        for good in goodList:
            row = Good(title = good['text'], link = good['link'], category = subCat['text'])
            db.session.add(row)
            db.session.commit()

    return ''' {'status': 'ok'} '''

@app.route('/')
def home():
    data = Good.query.all()
    return render_template('home.html', data=data)