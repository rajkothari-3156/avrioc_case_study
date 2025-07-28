import random
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
import os

random.seed(0)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

user_ids = [f"user_{str(i).zfill(4)}" for i in range(9999)]
item_ids = [f"item_{str(i).zfill(4)}" for i in range(50)]
interaction_types = ['open_app','login','view','click','payment_initiated','purchase']
interaction_types_weights = [0.4,0.25,0.2,0.1,0.08,0.02]
timestamps = [datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(1000)]
experiments = ['Optimized-conversion','Optimized-revenue','Optimized-revenue-per-click','Optimized-revenue-per-view','Optimized-revenue-per-purchase']
experiment_variations = ['A','B','C','D','E']
session_ids = [f"session_{str(i).zfill(4)}" for i in range(9999)]
device_names = ['iPhone','Android','Desktop','Tablet']



def generate_data(batch_size,time_interval,data_generation_speed):
    data = []
    for i in range(batch_size):
        user_id = random.choice(user_ids)
        item_id = random.choice(item_ids)
        interaction_type = random.choices(interaction_types,weights=interaction_types_weights)[0]
        timestamp = random.choice(timestamps).strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(time_interval/data_generation_speed)
        data.append({
            'user_id': user_id,
            'item_id': item_id,
            'interaction_type': interaction_type,
            'timestamp': timestamp,
            'metadata': {
                'experiment_name': random.choice(experiments),
                'experiment_variation': random.choice(experiment_variations),
                'session_id': random.choice(session_ids),
                'device_name': random.choice(device_names)
                
            }
        })
    return data

if __name__ == '__main__':
    data = generate_data()
    