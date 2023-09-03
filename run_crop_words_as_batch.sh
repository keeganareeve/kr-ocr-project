#!/bin/bash
# Run with 'bash run_crop_words_as_batch.sh'
# Make sure to change inputdir, input_file, outputdir
# (I have the below as defaults to showcase usage)
inputdir="./output_pngs/fullpages"
input_file="input.txt"
outputdir="./output_pngs"

# =() initializes array in bash
names=()

# Checks if input file is a file (-f)
if [ ! -f "$input_file" ]; then
  echo "Input file not found: $input_file"
  exit 1
fi

# Read each line from the input file
while IFS= read -r line; do
  # Extracts name (before extension) from line
  # (##.* would be used for the extension itself)
  name="${line%.*}"
  
  # Adds name to names array
  names+=("$name")

done < "$input_file"
if [ ! -d "$outputdir" ]; then
  echo "Base directory doesn't exist: $outputdir"
  exit 1
fi

for ((i=0; i<${#names[@]}; i++)); do
  # Combines base directory with current string
  name="${names[i]}"
  combined_dir="$outputdir/$name"

  # Finds PNG file that will be the input for crop_words.py
  current_input="$inputdir"/"$name"".png"
  echo "Input page (as png): ""$current_input"
  echo "Ouput directory: ""$combined_dir"

  # Checks if directory exists and runs crop_words.py script (-d)
  if [ ! -d "$combined_dir" ]; then
    mkdir -p "$combined_dir"
    echo "Created directory: $combined_dir"
    python3 crop_words.py "$current_input" "$combined_dir"/
  else
    echo "Directory already exists: $combined_dir"
    python3 crop_words.py "$current_input" "$combined_dir"/
  fi
done