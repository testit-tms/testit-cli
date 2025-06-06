import os
import tempfile
import pytest
from unittest.mock import Mock

from src.testit_cli.service import Service
from src.testit_cli.models.config import Config


@pytest.fixture
def mock_config():
    """Fixture for creating mock config object"""
    config = Mock(spec=Config)
    return config


@pytest.fixture  
def service(mock_config):
    """Fixture for creating Service instance with mock dependencies"""
    api_client = Mock()
    parser = Mock()
    importer = Mock()
    autotests_filter = Mock()
    
    return Service(
        config=mock_config,
        api_client=api_client,
        parser=parser,
        importer=importer,
        autotests_filter=autotests_filter
    )


def test_write_to_output_uses_utf8_encoding(service, mock_config):
    """Test verifies that file is written using UTF-8 encoding"""
    # Arrange
    cyrillic_content = "Тестовый контент с кириллицей: АБВГД абвгд"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_output_path = temp_file.name
    
    mock_config.output = temp_output_path
    
    try:
        # Act - call private method using name mangling
        service._Service__write_to_output(cyrillic_content)
        
        # Assert - verify file is written in UTF-8
        with open(temp_output_path, 'r', encoding='utf-8') as file:
            written_content = file.read()
            assert written_content == cyrillic_content
            
        # Additional check - read as bytes and verify UTF-8 BOM is absent
        with open(temp_output_path, 'rb') as file:
            raw_content = file.read()
            # Verify content can be decoded as UTF-8
            decoded_content = raw_content.decode('utf-8')
            assert decoded_content == cyrillic_content
            
    finally:
        # Cleanup
        if os.path.exists(temp_output_path):
            os.unlink(temp_output_path)


def test_write_to_output_creates_directory(service, mock_config):
    """Test verifies that directory is created if it doesn't exist"""
    # Arrange  
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "subdir", "output.txt")
        mock_config.output = output_path
        
        # Act
        service._Service__write_to_output("test content")
        
        # Assert
        assert os.path.exists(output_path)
        with open(output_path, 'r', encoding='utf-8') as file:
            assert file.read() == "test content" 