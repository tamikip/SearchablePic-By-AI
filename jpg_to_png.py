import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed


def convert_jpg_to_png(jpg_file_path, png_file_path):
    try:
        # Open the JPG image
        img = Image.open(jpg_file_path)

        # Save the image as PNG
        img.save(png_file_path, 'PNG')
        print(f"Successfully converted {jpg_file_path} to {png_file_path}")
    except Exception as e:
        print(f"Failed to convert {jpg_file_path}: {e}")


def batch_convert_jpg_to_png(input_folder, max_workers=10):
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filename in os.listdir(input_folder):
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                jpg_file_path = os.path.join(input_folder, filename)
                png_filename = os.path.splitext(filename)[0] + '.png'
                png_file_path = os.path.join(input_folder, png_filename)

                # Submit the conversion task to the thread pool
                futures.append(executor.submit(convert_jpg_to_png, jpg_file_path, png_file_path))

        # Optionally, wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()  # This will raise any exceptions caught during execution
            except Exception as e:
                print(f"Error during conversion: {e}")


# Example usage
input_folder = "path_to_your_folder"
batch_convert_jpg_to_png(input_folder)
