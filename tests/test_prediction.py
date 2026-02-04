import pytest
import os
from cnnClassifier.pipeline.prediction import PredictionPipeline
from pathlib import Path


def test_prediction_pipeline():
    # Path to a sample image (using one from artifacts)
    sample_image_path = "artifacts/data_ingestion/kidney-ct-scan-image/Normal/Normal- (637).jpg"
    
    # Check if the image exists before running the test
    if not os.path.exists(sample_image_path):
        pytest.skip(f"Sample image {sample_image_path} not found")

    # Initialize prediction pipeline
    pipeline = PredictionPipeline(filename=sample_image_path)
    
    # Run prediction
    result = pipeline.predict()
    
    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert "image" in result[0]
    assert result[0]["image"] in ["Normal", "Tumor"]
