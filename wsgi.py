from app import app, router
from app.controllers import *

print(app.url_map)
if __name__ == '__main__':
    app.register_blueprint(router)
    app.run()