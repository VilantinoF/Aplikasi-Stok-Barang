from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Barang(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100), nullable=False)
    jumlah_barang = db.Column(db.Integer, nullable=False)
    harga_beli_barang = db.Column(db.Integer, nullable=False)
    harga_jual_barang = db.Column(db.Integer, nullable=False)
    diskon = db.Column(db.Integer, nullable=False)
    jumlah_total = db.Column(db.Integer, nullable=False)
    tanggal_pembuatan = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Barang ' + str(self.nama_barang)

db.create_all()
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_barang = request.form['nama_barang']
        input_jumlah = request.form['jumlah_barang']
        input_harga_beli = request.form['harga_beli_barang']
        input_harga_jual = request.form['harga_jual_barang']
        input_diskon = request.form['diskon']
        jml_barang = (int(input_jumlah) * int(input_harga_beli)) * (1.0-(int(input_diskon)/100))
        post = Barang(nama_barang=input_barang, jumlah_barang=input_jumlah, harga_beli_barang=input_harga_beli, harga_jual_barang=input_harga_jual, diskon=input_diskon, jumlah_total=jml_barang)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        posts = Barang.query.order_by(Barang.tanggal_pembuatan).all()
        return render_template('index.html', posts=posts)

@app.route('/delete/<int:id>')
def delete(id):
    post_delete = Barang.query.get_or_404(id)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update(id):

    post = Barang.query.get_or_404(id)
    
    if request.method == 'POST':
        post.nama_barang = request.form['nama_barang']
        post.jumlah_barang = request.form['jumlah_barang']
        post.harga_beli_barang = request.form['harga_beli_barang']
        post.harga_jual_barang = request.form['harga_jual_barang']
        post.diskon = request.form['diskon']
        post.jumlah_total = (int(post.jumlah_barang) * int(post.harga_beli_barang)) * (1.0-(int(post.diskon)/100))
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', post=post)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.4')