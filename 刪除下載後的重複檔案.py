import os

# Define the directory path
directory = '/Users/david/Downloads/pdf2'

# List all files in the directory
files = os.listdir(directory)

# Loop through each file to find duplicates
for file in files:
    if file.endswith('_1.pdf'):
        # Construct the original and duplicate file paths
        original_file = os.path.join(directory, file.replace('_1', ''))
        duplicate_file = os.path.join(directory, file)

        # Check if the original file exists and compare sizes
        if os.path.exists(original_file) and os.path.getsize(original_file) == os.path.getsize(duplicate_file):
            # Remove the duplicate file if sizes are the same
            os.remove(duplicate_file)
            print(f"Deleted duplicate file: {duplicate_file}")
        else:
            print(f"No match found or size mismatch for: {duplicate_file}")