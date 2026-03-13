from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.routes.products_routes import products_bp  # noqa: E402


def create_app():
    from flask import Flask
    from app.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()
        _seed_products()

    return app


def _seed_products():
    """Insert initial plant catalog if the table is empty."""
    from app.models.product_model import Product

    if Product.query.count() > 0:
        return

    plants = [
        Product(
            name="Anturio Rojo",
            price=249.0,
            category="interior",
            image="anturio.png",
            care="☀️ Luz indirecta · 💧 Semanal",
            badge="Popular",
            badge_type=None,
            original_price=None,
        ),
        Product(
            name="Monstera Deliciosa",
            price=349.0,
            category="tropical",
            image="monstera.png",
            care="☀️ Luz indirecta · 💧 Semanal",
            badge="Nuevo",
            badge_type="new",
            original_price=None,
        ),
        Product(
            name="Peperomia Watermelon",
            price=129.0,
            category="interior",
            image="peperomia.png",
            care="☀️ Luz indirecta · 💧 Cada 10 días",
            badge=None,
            badge_type=None,
            original_price=None,
        ),
        Product(
            name="Pothos Dorado",
            price=99.0,
            category="interior",
            image="pothos.png",
            care="☀️ Poca luz · 💧 Semanal",
            badge="-20%",
            badge_type="sale",
            original_price=125.0,
        ),
        Product(
            name="Rosa del Desierto",
            price=299.0,
            category="suculenta",
            image="rosa_desierto.png",
            care="☀️ Sol directo · 💧 Quincenal",
            badge="Exótica",
            badge_type=None,
            original_price=None,
        ),
        Product(
            name="Suculenta Echeveria",
            price=89.0,
            category="suculenta",
            image="succulent.png",
            care="☀️ Sol directo · 💧 Quincenal",
            badge="Popular",
            badge_type=None,
            original_price=None,
        ),
        Product(
            name="Helecho de Boston",
            price=199.0,
            category="helecho",
            image="helecho.png",
            care="🌥️ Sombra parcial · 💧 Frecuente",
            badge="-20%",
            badge_type="sale",
            original_price=249.0,
        ),
        Product(
            name="Cactus San Pedro",
            price=159.0,
            category="suculenta",
            image="cactus.png",
            care="☀️ Sol directo · 💧 Mensual",
            badge=None,
            badge_type=None,
            original_price=None,
        ),
        Product(
            name="Orquídea Phalaenopsis",
            price=279.0,
            category="tropical",
            image="orquidea.png",
            care="☀️ Luz indirecta · 💧 Cada 10 días",
            badge="Nuevo",
            badge_type="new",
            original_price=None,
        ),
        Product(
            name="Ficus Lyrata",
            price=399.0,
            category="interior",
            image="ficus.png",
            care="☀️ Luz brillante · 💧 Semanal",
            badge="Popular",
            badge_type=None,
            original_price=None,
        ),
    ]

    db.session.bulk_save_objects(plants)
    db.session.commit()
