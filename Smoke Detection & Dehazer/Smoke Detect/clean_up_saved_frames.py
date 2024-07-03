# Clean up: Delete all saved frames
for filename in os.listdir(input_directory):
    file_path = os.path.join(input_directory, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

for filename in os.listdir(output_directory):
    file_path = os.path.join(output_directory, filename) 
    if os.path.isfile(file_path):
        os.remove(file_path)

# Optionally, remove the empty directories
os.rmdir(input_directory)
os.rmdir(output_directory)
