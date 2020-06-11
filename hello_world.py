from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_barang.db'
db = SQLAlchemy(app)

class Barang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String, nullable=False)
    jumlah_barang = db.Column(db.Integer, nullable=False, default=1)
    harga_barang = db.Column(db.String, nullable=False)
    tanggal_pembuatan = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)