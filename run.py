from cashier_service import app
from cashier_service.infrastructure.event_publisher import EventPublisher
from cashier_service.settings import config, Config

if __name__ == "__main__":
    broker = EventPublisher(config['development'])
    app.create(config=config['development'],
               broker=broker).run(
        host='0.0.0.0', port=int(Config.PORT))
