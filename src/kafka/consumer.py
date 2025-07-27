from kafka import KafkaConsumer
import json
import sys
import os
import clickhouse_connect
import time
import pandas as pd
module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)

def main():
    data = []
    topic_name = os.getenv('KAFKA_TOPIC')
    consumer_timeout_ms = 10000
    flush_interval = 5
    batch_size = 1000
    kafka_broker_url = os.getenv('KAFKA_BROKER_URL')
    last_flush_time = time.time()
    

    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=kafka_broker_url,
        auto_offset_reset='latest',
        consumer_timeout_ms=consumer_timeout_ms,
        enable_auto_commit=True,  
        auto_commit_interval_ms=1000,
    )
    

    message_count = 0
    retries = 0
    while retries<3:
        msg_pack = consumer.poll(timeout_ms=consumer_timeout_ms,)

        if msg_pack:
            print(f"Received {len(msg_pack)} messages")
            for topic_partition, messages in msg_pack.items():
                
                for message in messages:
                    
                    data.append(json.loads(message.value.decode('utf-8')))
                    message_count += 1
                    if message_count>batch_size or time.time() - last_flush_time > flush_interval:
                        print(f"Flushing {len(data)} messages to ClickHouse")
                        flush_to_clickhouse(data)
                        message_count = 0
                        data = []
                        last_flush_time = time.time()

                
        else:
            print('No messages received in this poll, retrying')
            print(f'Total messages received: {message_count}')
            retries += 1
            time.sleep(1)
    print(f'Flushing {len(data)} messages to ClickHouse for the final time before closing')
    flush_to_clickhouse(data)
    
    consumer.close()
    return data 
    
    
def flush_to_clickhouse(data):
    if data:
        clickhouse_client = clickhouse_connect.get_client(
            host=os.getenv('CLICKHOUSE_HOST'),
            user=os.getenv('CLICKHOUSE_USER'),
            password=os.getenv('CLICKHOUSE_PASSWORD'),
            secure=True
        )
        
        # Create table matching your data generator structure
        
        clickhouse_client.command('''
            CREATE TABLE IF NOT EXISTS default.clickstream_data (
                user_id String,
                item_id String, 
                interaction_type String,
                timestamp String
            )
            ENGINE = MergeTree()
            ORDER BY (user_id, timestamp)
        ''')
        
        clickhouse_client.insert('default.clickstream_data', pd.DataFrame(data))
        print(f"Inserted {len(data)} rows into ClickHouse")
        


if __name__ == '__main__':
    main()

      