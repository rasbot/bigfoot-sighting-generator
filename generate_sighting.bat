#!/bin/bash

python sample.py --save_dir="data/observed/save" -n=250 -s=True -t="observed"
python sample.py --save_dir="data/environment/save" -n=30 -s=True -t="environment"
python sample.py --save_dir="data/time_conditions/save" -n=20 -s=True -t="time_conditions"

python generate_sighting.py