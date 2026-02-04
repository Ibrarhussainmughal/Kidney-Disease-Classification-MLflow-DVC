import os
import zipfile
import gdown
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> str:
        """
        Downloads the dataset from a Google Drive link.
        """
        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file

            # ✅ Ensure the parent directory exists before downloading
            os.makedirs(os.path.dirname(zip_download_dir), exist_ok=True)

            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            # Extract the file ID from the Google Drive link
            file_id = dataset_url.split("/")[-2]
            download_url = f'https://drive.google.com/uc?id={file_id}'

            # ✅ Download using gdown
            gdown.download(download_url, zip_download_dir, quiet=False)

            # ✅ Check if the file was downloaded successfully
            if not os.path.exists(zip_download_dir):
                raise FileNotFoundError(f"Download failed. File not found: {zip_download_dir}")

            logger.info(f"Successfully downloaded data from {dataset_url} into file {zip_download_dir}")
            return zip_download_dir

        except Exception as e:
            logger.error(f"Error in downloading file: {str(e)}")
            raise e

    def extract_zip_file(self):
        """
        Extracts the ZIP file into the specified directory.
        """
        try:
            unzip_path = self.config.unzip_dir

            # ✅ Ensure the directory exists before extracting
            os.makedirs(unzip_path, exist_ok=True)

            # ✅ Check if the ZIP file exists before extracting
            if not os.path.exists(self.config.local_data_file):
                raise FileNotFoundError(f"ZIP file not found: {self.config.local_data_file}")

            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)

            logger.info(f"Extracted data to: {unzip_path}")

        except zipfile.BadZipFile:
            logger.error("Error: Corrupted ZIP file. Extraction failed.")
        except Exception as e:
            logger.error(f"Error in extracting ZIP file: {str(e)}")
            raise e