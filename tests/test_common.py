import pytest
from pathlib import Path
from cnnClassifier.utils.common import read_yaml, create_directories
from box import ConfigBox
import os
import yaml


def test_read_yaml(tmp_path):
    # Create a temporary yaml file
    d = {"key": "value"}
    yaml_file = tmp_path / "test.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(d, f)
    
    # Test reading the yaml file
    result = read_yaml(Path(yaml_file))
    assert isinstance(result, ConfigBox)
    assert result.key == "value"


def test_read_yaml_empty(tmp_path):
    # Create an empty temporary yaml file
    yaml_file = tmp_path / "empty.yaml"
    with open(yaml_file, "w") as f:
        pass
    
    # Test reading the empty yaml file should raise ValueError
    with pytest.raises(ValueError):
        read_yaml(Path(yaml_file))


def test_create_directories(tmp_path):
    # Create a list of temporary directories
    path1 = tmp_path / "dir1"
    path2 = tmp_path / "dir2"
    paths = [str(path1), str(path2)]
    
    # Test creating directories
    create_directories(paths)
    assert os.path.exists(path1)
    assert os.path.exists(path2)
