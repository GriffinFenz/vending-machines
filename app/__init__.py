from flask import Flask
from app.extensions import db, Base, Engine, Session
from app.models.vending_machine import VendingMachine
from app.models.product import Product
from app.models.machine_stock import MachineStock
from config import Config
import sys

sys.path.append('../')


def drop_tables():
    session = Session()
    Base.metadata.drop_all()
    session.close()


def insert_sample_data():
    with Session() as session:
        session.add(VendingMachine.create(session, 'front of school').item)
        session.add(VendingMachine.create(session, 'back of school').item)
        session.add(VendingMachine.create(session, 'my house').item)
        session.add(Product.create(session, 'coke', '20').item)
        session.add(Product.create(session, 'taro', '15').item)
        session.add(Product.create(session, 'chocolate', '50').item)
        session.add(Product.create(session, 'robert', '55.80').item)
        session.add(Product.create(session, 'nail clippers', '800.12345678').item)
        session.commit()

        ms1 = MachineStock(machine_id=1, product_id=1, quantity=50)
        ms2 = MachineStock(machine_id=2, product_id=3, quantity=1)
        ms3 = MachineStock(machine_id=3, product_id=2, quantity=2000)
        ms4 = MachineStock(machine_id=1, product_id=2, quantity=2)
        session.commit()

        session.add(ms1)
        session.add(ms2)
        session.add(ms3)
        session.add(ms4)
        session.commit()


def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object(Config)
    # Initialize Flask extensions here
    db.init_app(app)

    # Drop and create tables to put in the database server
    app.app_context().push()
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)

    # Sample data to add in for testing
    # Comment out the line below for production
    insert_sample_data()

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.machine_stock import bp as machine_stock_bp
    app.register_blueprint(machine_stock_bp)

    from app.vending_machine import bp as vending_machine_bp
    app.register_blueprint(vending_machine_bp)

    from app.product import bp as product_bp
    app.register_blueprint(product_bp)

    @app.route('/')
    def index():
        return "welcome to the API! :)"

    print('DEBUG: app starting')
    return app
