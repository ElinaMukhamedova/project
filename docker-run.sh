#!/bin/zsh
docker run \
    -v  $PWD/submodules:/app/submodules \
    -v  $PWD/dagflow:/app/dagflow \
    -v  $PWD/dgf_statistics:/app/dgf_statistics \
    -v  $PWD/multikeydict:/app/multikeydict \
    -v  $PWD/models:/app/models \
    -v  $PWD/scripts:/app/scripts \
    -v  $PWD/statistical_methods:/app/statistical_methods \
    -v  $PWD/illustrations:/app/illustrations \
    -it dagflow:v00 /bin/bash

