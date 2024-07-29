#!/bin/bash

# Output file
output_file="py_files_content.txt"

# Clear the output file if it exists
> "$output_file"

# Find all .py files in the current directory and subdirectories
find . -type f -name "*.py" | while read -r file; do
  # Append the file content to the output file
  echo "Content of $file:" >> "$output_file"
  echo "=================" >> "$output_file"
  cat "$file" >> "$output_file"
  echo "=================" >> "$output_file"
  echo >> "$output_file"
done

echo "Contents of all .py files have been saved to $output_file"