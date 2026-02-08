import logging
import os

from flask import Flask, abort, render_template, request, send_from_directory

app = Flask(__name__)

payloads_dir = os.path.abspath(os.getenv("DYNASTY_PAYLOADS_DIR", "payloads"))

logging.basicConfig(
    level=os.getenv("DYNASTY_WEB_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("dynasty.web")


def list_payloads():
    if not os.path.isdir(payloads_dir):
        logger.warning("Payload directory missing: %s", payloads_dir)
        return []
    return sorted(
        file
        for file in os.listdir(payloads_dir)
        if os.path.isfile(os.path.join(payloads_dir, file))
    )


@app.route('/')
def index():
    files = list_payloads()
    return render_template('index.html', files=files)


@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    files = list_payloads()
    filtered_files = [file for file in files if query in file.lower()]
    return render_template('index.html', files=filtered_files, query=query)


@app.route('/payloads/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(payloads_dir, filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(payloads_dir, filename)


if __name__ == '__main__':
    app.run(
        host=os.getenv("DYNASTY_WEB_HOST", "0.0.0.0"),
        port=int(os.getenv("DYNASTY_WEB_PORT", "5000")),
        debug=False,
    )
