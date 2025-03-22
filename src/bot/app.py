import argparse
import asyncio


from ..utils.ConfigLoader import load_config
from .bot import start_bot

def parse_arguments():
    parser = argparse.ArgumentParser(description='Hermes bot.')
    parser.add_argument(
        '-c', '--config_file', type=str, default='src/configs/bot_config.yaml', help='Bot configuretion file'
    )
    

    args = parser.parse_args()

    return args

 

if __name__ == '__main__':
    args = parse_arguments()
    cfg = load_config(args.config_file)


    asyncio.run(start_bot(cfg))
     
