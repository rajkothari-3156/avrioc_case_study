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
interaction_types = ['click','view','purchase']
timestamps = [datetime.now() - timedelta(days=random.randint(0, 1)) for _ in range(1000)]


def generate_data(batch_size,time_interval,data_generation_speed):
    data = []
    for i in range(batch_size):
        user_id = random.choice(user_ids)
        item_id = random.choice(item_ids)
        interaction_type = random.choice(interaction_types)
        timestamp = random.choice(timestamps).strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(time_interval/data_generation_speed)
        data.append({
            'user_id': user_id,
            'item_id': item_id,
            'interaction_type': interaction_type,
            'timestamp': timestamp})
    return data

if __name__ == '__main__':
    data = generate_data()
    