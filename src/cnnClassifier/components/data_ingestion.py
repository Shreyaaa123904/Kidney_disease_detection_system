import os
import zipfile
from pathlib import Path
import gdown
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import (DataIngestionConfig)



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def _dataset_dir(self) -> Path:
        return Path(self.config.unzip_dir) / "kidney-ct-scan-image"

    def _is_dataset_available(self) -> bool:
        dataset_dir = self._dataset_dir()
        return dataset_dir.exists() and any(dataset_dir.iterdir())

    
    def download_file(self)-> str:
        '''
        Fetch data from the url
        '''

        try: 
            if self._is_dataset_available():
                logger.info(f"Dataset already available at {self._dataset_dir()}; skipping download.")
                return

            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix+file_id,zip_download_dir)

            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            raise e
        
    

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        if self._is_dataset_available():
            logger.info(f"Dataset already extracted at {self._dataset_dir()}; skipping extraction.")
            return

        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        if not Path(self.config.local_data_file).exists():
            raise FileNotFoundError(
                f"Expected archive not found at {self.config.local_data_file}. "
                "Place the dataset zip there or restore network access to download it."
            )

        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)