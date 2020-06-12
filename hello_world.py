from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_barang.db'
db = SQLAlchemy(app)

class Barang(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100), nullable=False)
    jumlah_barang = db.Column(db.Integer, nullable=False, default=1)
    harga_barang = db.Column(db.Integer, nullable=False)
    jumlah_total = db.Column(db.Integer, nullable=False)
    tanggal_pembuatan = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'ID Barang' + str(self.id)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_barang = request.form['nama_barang']
        input_jumlah = request.form['jumlah_barang']
        input_harga = request.form['harga_barang']
        jml_total = int(input_harga)*int(input_jumlah)
        post = Barang(nama_barang=input_barang, jumlah_barang=input_jumlah, harga_barang=input_harga, jumlah_total=jml_total)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        posts = Barang.query.(Barang.tanggal_pembuatan).all()
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
        post.harga_barang = request.form['harga_barang']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', post=post)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.4')