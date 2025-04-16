#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR1="$SCRIPT_DIR/examples"
DIR2="$SCRIPT_DIR/presentation_examples"
# DIR1="$SCRIPT_DIR"  # Placeholder
# DIR2="$SCRIPT_DIR"  # Placeholder

# -- Function to compile LaTeX files in a given directory
compile_latex() {
    local dir=$1
    echo "Compiling LaTeX files in directory: $dir"
    for file in "$dir"/*.tex; do
        if [ -f "$file" ]; then
            echo "Processing $file..."
            pdflatex -halt-on-error -output-directory="$dir" "$file"
            if [ $? -ne 0 ]; then
                echo "Error compiling $file. Compilation halted."
                exit 1
            fi
        else
            echo "No .tex files found in $dir."
        fi
    done
}

# Compile LaTeX files in both directories
compile_latex "$DIR1"
compile_latex "$DIR2"

echo "Compilation of all LaTeX files completed."