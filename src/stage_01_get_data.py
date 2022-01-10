import argparse
import os
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import urllib.request as req


STAGE = "stage_01_get_data" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def get_data(config_path):
    ## read config files
    config = read_yaml(config_path)
    source_data_url = config["source_data_url"]
    
    local_data_dir = config["source_data_dir"]["data_dir"]
    local_data_file = config["source_data_dir"]["data_file"]
    create_directories([local_data_dir])

    local_data_file_path = os.path.join(local_data_dir,local_data_file)

    logging.info("Download started......")
    filename,headers = req.urlretrieve(source_data_url,local_data_file_path)
    logging.info(f"Download completed")
    logging.info(f"Download file is present at: {filename}")
    logging.info(f"Download headers: \n{headers}")


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        get_data(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e