import os.path
from dotenv import load_dotenv

from pointsheet import create_app

if os.path.exists('.env'):
    load_dotenv()



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)