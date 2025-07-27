import os
import sys
import json
from datetime import datetime
import pandas as pd
import numpy as np
import time
module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)
from src.kafka.consumer import create_consumer,flush_to_clickhouse
from src.slack_alerts.monitor_item_sales import monitor_item_sales

def main():
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS default.fct_item (
    batch_id String,
    event_date Date,
    item_id String,
    total_interactions int,
    total_purchases int,
    total_views int,
    total_clicks int
    )
    ENGINE = MergeTree()
    ORDER BY (event_date, item_id)

    '''
    table_name = 'default.fct_item'
    retries = 0
    consumer_timeout_ms = int(os.getenv('KAFKA_CONSUMER_TIMEOUT_MS'))

    consumer = create_consumer(group_name='fct_item_consumer')
    data = []

    while retries<3:
        msg_pack = consumer.poll(timeout_ms=consumer_timeout_ms,)

        if msg_pack:
            batch_id = str(datetime.now().strftime('%Y%m%d%H%M%S'))
            print(f"Received {len(msg_pack)} messages")
            for topic_partition, messages in msg_pack.items():
                for message in messages:
                    message_data = json.loads(message.value.decode('utf-8'))
                    message_data['item_id'] = message_data['item_id']
                    data.append(message_data)
            print(f"Flushing {len(data)} messages to ClickHouse")
            df = pd.DataFrame(data)
            df['batch_id'] = [batch_id]*len(df)
            df['event_date'] = pd.to_datetime(df['timestamp'].str[:10])
            df['item_id'] = df['item_id']
            df['total_interactions'] = [1]*len(df)
            df['total_purchases'] = np.where(df['interaction_type'] == 'purchase', 1, 0)
            df['total_views'] = np.where(df['interaction_type'] == 'view', 1, 0)
            df['total_clicks'] = np.where(df['interaction_type'] == 'click', 1, 0)
            
            item_df = df.groupby(['batch_id','event_date','item_id']).agg({
                'total_interactions': 'sum',
                'total_purchases': 'sum',
                'total_views': 'sum',
                'total_clicks': 'sum'
            }).reset_index()


            flush_to_clickhouse(item_df,create_table_sql,table_name)
        else:
            print('No messages received in this poll, retrying')
            retries += 1
            time.sleep(1)
    return data

if __name__ == '__main__':
    main()
    monitor_item_sales()