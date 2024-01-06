import subprocess
import json

def get_image_rating(image_path):
    try:
        # Run ExifTool command to get JSON metadata
        exiftool_command = ['exiftool', '-j', image_path]
        result = subprocess.run(exiftool_command, capture_output=True, text=True, check=True)

        # Parse the JSON output
        metadata_list = json.loads(result.stdout)

        # Look for the Rating tag in the metadata
        for metadata in metadata_list:
            if 'Rating' in metadata:
                return metadata['Rating']

        # If Rating tag is not found, return None
        return None

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# Example usage
image_path = 'img.jpg'
rating = get_image_rating(image_path)

if rating is not None:
    print(f"The rating of the image is: {rating}")
else:
    print("Rating information not found or there was an error.")
