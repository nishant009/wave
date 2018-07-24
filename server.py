import glob
import os
import optparse

from pathlib import Path
from flask import Flask, request, redirect, flash, render_template, url_for, session
from werkzeug.utils import secure_filename

from db_util import DBUtil
from parser import Parser
from report_generator import ReportGenerator

UPLOAD_FOLDER = str(Path('.')) + '/files'
TEMPLATE_FOLDER = str(Path('.')) + '/templates'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['TEMPLATE_FOLDER'] = TEMPLATE_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_util = None

@app.route('/', methods=['GET'])
def index():
    results = _get_report()
    return render_template('index.html', value = results)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        return _process_file()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    _shutdown_server()
    return 'Server shutting down...'

def _get_report():
    report_generator = ReportGenerator(db_util)
    return report_generator.generate_report()

def _process_file():
    if 'csv_file' not in request.files:
        flash(u'No file provided', 'error')
        return redirect(url_for('index'))

    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        flash(u'No file selected', 'error')
        return redirect(url_for('index'))

    if csv_file and _allowed_file(csv_file.filename):
        file_name = os.path.join(
            UPLOAD_FOLDER,
            secure_filename(csv_file.filename)
        )
        try:
            csv_file.save(file_name)
    
            parser = Parser(db_util, file_name)

            if parser.process():
                flash(u'Success', 'success')
                return redirect(url_for('index'))
            else:
                flash(u'Failure', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash(u'Duplicate report', 'error')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash(u'File processing failed', 'error')
            return redirect(url_for('index'))

def _shutdown_server():
    session.pop('_flashes', None)
    try:
        for f in Path(UPLOAD_FOLDER).glob('*.csv'):
            os.remove(f)
        
        db_util.close()
    except Exception:
        print('Could not perform clean shutdown!')

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def setup():
    parser = optparse.OptionParser()
    parser.add_option(
        '-t',
        '--host',
        action='store',
        dest='host',
        help='MySQL host',
        default='localhost'
    )
    parser.add_option(
        '-u',
        '--user',
        action='store',
        dest='user',
        help='MySQL user',
        default='guest'
    )
    parser.add_option(
        '-p',
        '--password',
        action='store',
        dest='password',
        help='MySQL password',
        default=''
    )
    parser.add_option(
        '-d',
        '--db',
        action='store',
        dest='database',
        help='Redis database',
        default='wave'
    )
    options, _ = parser.parse_args()

    try:
        instance = DBUtil(
            options.host,
            options.user,
            options.password,
            options.database
        )

        return instance
    except RuntimeError as error:
        print(error.args)
        raise

if __name__ == "__main__":
    try:
        db_util = setup()
        app.run(host='0.0.0.0')
    except RuntimeError as error:
        raise