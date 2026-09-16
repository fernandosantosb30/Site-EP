from flask import Flask
from datetime import datetime, timezone
from config.settings import Config
from routes.main import main_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    app.register_blueprint(main_bp)

    @app.context_processor
    def site_context():
        return {"current_year": datetime.now(timezone.utc).year, "static_export": False}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
