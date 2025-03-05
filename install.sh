#!/bin/bash

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "export TEXINPUTS=':$SOURCE_DIR'" >> ~/.bashrc

echo "Updated TEXINPUTS."