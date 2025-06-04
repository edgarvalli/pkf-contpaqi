from app import app
from app_types import Config

def main():
    config = Config()
    config.init_from_jsonfile()
    app.config['appconfig'] = config.to_dict()
    app.run(**config.server.__dict__)

if __name__ == "__main__":
    main()