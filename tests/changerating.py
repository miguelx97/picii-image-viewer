import os
from PIL import Image
import xml.etree.ElementTree as ET

# selected_folder = '/home/miguel/Pictures'
# image_files = [f for f in os.listdir(selected_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

current_image_index = 0
# current_image = os.path.join(selected_folder, image_files[current_image_index])
image_filename = 'img.jpg'
print('Current image:', image_filename)

def get_image_rating(filename):
    try:
        # Open the image file
        img = Image.open(filename)

        # Get the XMP metadata
        xmp_data = img.info.get('Xmp', None)

        print(xmp_data[:100])

        if xmp_data:
            # Parse the XMP XML data
            xmp_tree = ET.fromstring(xmp_data)
            
            # Define the XMP namespace
            xmp_namespace = {'xmp': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}

            # Find the rating tag and extract its value
            rating_tag = xmp_tree.find('.//xmp:Rating', namespaces=xmp_namespace)

            if rating_tag is not None and 'Rating' in rating_tag.attrib:
                return int(rating_tag.attrib['Rating'])

    except Exception as e:
        print(f"Error: {e}")

    return None

# Example usage
rating = get_image_rating(image_filename)

if rating is not None:
    print(f"The rating of {image_filename} is: {rating}")
else:
    print(f"No rating found for {image_filename}")