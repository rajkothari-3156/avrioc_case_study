#!/bin/bash


python src/kafka/producer.py --batch_size 10000 --data_generation_speed 10000 &
python src/data_models/fct_user.py &
python src/data_models/fct_item.py &
python src/data_models/fct_experiment.py &

echo "All processes started"
wait 