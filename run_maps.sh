#!/bin/bash

INPUT_FOLDER="/data/Twitter dataset"
OUTPUT_FOLDER="outputs"

for file in "$INPUT_FOLDER"/geoTwitter20-*.zip; do
    echo "Processing $file"
    nohup python3 src/map.py --input_path "$file" --output_folder "$OUTPUT_FOLDER" &
done

echo "All mapping jobs submitted."
