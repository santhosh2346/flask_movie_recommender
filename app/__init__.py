from flask import Flask

def create_app():
    app = Flask(__name__)

    from .api import api_bp
    app.register_blueprint(api_bp)

    @app.route("/ui")
    def ui():
        from flask import render_template
        return render_template("ui.html")

    return app
