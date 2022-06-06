from main import App
from .index_bp import index_bp

app = App.get_app()

app.register_blueprint(index_bp)

