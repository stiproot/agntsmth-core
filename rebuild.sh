#!/bin/bash

rm -rf dist/

python -m build

cd dist/

tar -xvf *.tar.gz -C .
