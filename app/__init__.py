from flask import Flask, redirect, url_for
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.auth import auth_bp
    from app.routes.seller import seller_bp
    from app.routes.buyer import buyer_bp
    from app.routes.marketplace import marketplace_bp
    from app.routes.escrow import escrow_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(escrow_bp)
    app.register_blueprint(admin_bp)


    @app.route("/")
    def index():
        return redirect(url_for("auth.landing"))

    return app