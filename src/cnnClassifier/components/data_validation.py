import os
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    def validate_all_files_exist(self)-> bool:
        try:
            validation_status = True
            all_files = os.listdir(self.config.unzip_dir)

            for file in self.config.ALL_REQUIRED_FILES:
                if file not in all_files:
                    validation_status = False
                    break
            
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        
        except Exception as e:
            raise e
