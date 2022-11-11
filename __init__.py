from api.views import api_blueprint
from views import app

app.register_blueprint(api_blueprint)