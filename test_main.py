import pytest
import os

# Import the functions from your web application code
from main import img_summary, load_model, YOLO


# Test img_summary function
@pytest.mark.parametrize(
    "field, expected_result", [
        ('file_name', 'labels'),
        ('total_stones', 2),
        ('avg_width', pytest.approx(0.35 * 409, rel=1e-2)),
        ('avg_height', pytest.approx(0.45 * 518, rel=1e-2))
        ]
        )
def test_img_summary(field, expected_result):
    # Create a temporary label file for testing
    test_labels = "1 0.2 0.3 0.4 0.5\n2 0.1 0.2 0.3 0.4\n"
    with open('test_labels.txt', 'w') as f:
        f.write(test_labels)

    # Call the img_summary function with the temporary label file
    result = img_summary('test_labels.txt')

    # Assert the expected values
    assert result[field][0] == expected_result

    # Remove the temporary label file
    os.remove('test_labels.txt')


# Test load_model function
def test_model_isnt_none():
    model = load_model()
    # Assert that the model is loaded successfully
    assert model is not None


def test_model_is_yolo():
    model = load_model()
    assert isinstance(model, YOLO)  # Replace YOLO with the actual model class
