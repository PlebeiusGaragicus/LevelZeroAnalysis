#!/bin/bash

output_file="output.csv"

# Check if output file already exists, if so, remove it
if [ -f "$output_file" ]; then
    rm "$output_file"
fi

# Get the header from the first CSV file
# This assumes that all files have the same header and it's on the first line
header_set=false
for input_file in *.csv; do
    if [ "$header_set" = false ]; then
        head -n 1 "$input_file" > "$output_file"
        header_set=true
    fi
    # Skip the header and append the rest to the output file
    tail -n +2 "$input_file" >> "$output_file"
done

echo "All CSV files have been concatenated into $output_file"
