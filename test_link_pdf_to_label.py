import pytest
import os
from link_pdf_to_label import check_for_pdf

def test_check_for_pdf():
    # Set up
    folder = r''
    placemark_name = 'test_pdf'  # Make sure this file exists in the folder

    # Call the function with the test parameters
    result = check_for_pdf(folder, placemark_name)

    # Assert that the function returns True (since the file should exist)
    assert result

# Run the test with: pytest -v test_link_pdf_to_label.py
