from . import run
from . import config
from . import data_lookup
import argparse

if __name__ == '__main__':
    # Parse config path
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, help="Path to config", default='./config.json')

    args = parser.parse_args()

    try:
        # Init config
        config.init(args.c)
    except Exception as e:
        app.logger.error(f"Failed to load config! {e}")
        sys.exit(1)

    # Init data lookup
    data_lookup.init(config.get())

    # Run server
    run()