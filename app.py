from flask import Flask, render_template, request, redirect, url_for, session
import os
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)

sticker_packs = [
    {
        'name': 'Pack 1',
        'stickers': ['sticker1.webp'],
        'key': 'd2a0a0d3e3e3e3e3d2a0a0d3e3e3e3e3'
    }
]

@app.route('/')
def index():
    return render_template('index.html', sticker_packs=sticker_packs)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' in session:
        return render_template('admin.html', sticker_packs=sticker_packs)
    if request.method == 'POST':
        if request.form.get('password') == 'password':
            session['logged_in'] = True
            return render_template('admin.html', sticker_packs=sticker_packs)
        else:
            return redirect(url_for('index'))
    return render_template('login.html')

import secrets

@app.route('/add_pack', methods=['POST'])
def add_pack():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    pack_name = request.form.get('name')
    if pack_name:
        pack_key = secrets.token_hex(16)
        sticker_packs.append({'name': pack_name, 'stickers': [], 'key': pack_key})
        os.makedirs(os.path.join('static', 'stickers', pack_name))
    return redirect(url_for('admin'))

@app.route('/whatsapp_instructions')
def whatsapp_instructions():
    return render_template('whatsapp_instructions.html')

if __name__ == '__main__':
    app.run(debug=True)
