import os.path
from dotenv import load_dotenv

from pointsheet import create_app


debug = False

if os.path.exists('.env'):
    load_dotenv()

if os.environ.get('APP_ENV', 'dev') != 'prod':
    debug = True



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=debug, load_dotenv=True)