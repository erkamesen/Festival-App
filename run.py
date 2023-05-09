from apps import create_app, db
from config import Config
from flask_migrate import Migrate



app = create_app(config=Config)
Migrate(app, db)


app.run()