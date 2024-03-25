import os

from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

payloads_dir = 'payloads'

@app.route('/')
def index():
    files = os.listdir(payloads_dir)
    return render_template('index.html', files=files)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    files = os.listdir(payloads_dir)
    filtered_files = [file for file in files if query in file.lower()]
    return render_template('index.html', files=filtered_files, query=query)

@app.route('/payloads/<path:filename>')
def serve_file(filename):
    return send_from_directory(payloads_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)

