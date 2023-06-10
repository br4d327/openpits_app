import pytest
import os
from PIL import Image

# Import the functions from your web application code
from main import img_summary, load_model, image_input, YOLO

# Test img_summary function
@pytest.mark.parametrize("field, expected_result", 
                        [('file_name', 'labels'),
                        ('total_stones', 2),
                        ('avg_width', pytest.approx(0.35 * 409, rel=1e-2)),
                        ('avg_height', pytest.approx(0.45 * 518, rel=1e-2))])
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


# Test image_input function
# def test_image_input_single_file():
#     # Create a temporary image file for testing
#     image_data = Image.new('RGB', (100, 100))
#     image_data.save('test_image.jpg')

#     # Create a mock file uploader
#     class MockFileUploader:
#         def __init__(self, name):
#             self.name = name

#         def getbuffer(self):
#             with open(self.name, 'rb') as f:
#                 return f.read()

#     # Call the image_input function with the mock file uploader
#     image_path = image_input(MockFileUploader('test_image.jpg'), False)

#     # Assert the expected image path
#     assert image_path == 'data/uploads/test_image.jpg'

#     # Remove the temporary image file
#     os.remove('test_image.jpg')


# def test_image_input_multiple_files():
#     # Create temporary image files for testing
#     image_data1 = Image.new('RGB', (100, 100))
#     image_data1.save('test_image1.jpg')
#     image_data2 = Image.new('RGB', (100, 100))
#     image_data2.save('test_image2.jpg')

#     # Create mock file uploaders
#     class MockFileUploader:
#         def __init__(self, name):
#             self.name = name

#         def getbuffer(self):
#             with open(self.name, 'rb') as f:
#                 return f.read()

#     uploader1 = MockFileUploader('test_image1.jpg')
#     uploader2 = MockFileUploader('test_image2.jpg')

#     # Call the image_input function with the mock file uploaders
#     image_paths = image_input([uploader1, uploader2], True)

#     # Assert the expected image paths
#     assert image_paths == ['data/uploads/test_image1.jpg', 'data/uploads/test_image2.jpg']

#     # Remove the temporary image files
#     os.remove('test_image1.jpg')
#     os.remove('test_image2.jpg')

