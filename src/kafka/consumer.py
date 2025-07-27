from kafka import KafkaConsumer
import json
import sys
import os
import clickhouse_connect
import time
import pandas as pd
module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)



def create_consumer(group_name):
    consumer_timeout_ms = int(os.environ['KAFKA_CONSUMER_TIMEOUT_MS'])
    topic_name = os.getenv('KAFKA_TOPIC')
    kafka_broker_url = os.getenv('KAFKA_BROKER_URL')
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=kafka_broker_url,
        auto_offset_reset='latest',
        consumer_timeout_ms=consumer_timeout_ms,
        enable_auto_commit=True,  
        auto_commit_interval_ms=1000
    )
    return consumer


def main():
    data = []
    topic_name = os.getenv('KAFKA_TOPIC')
    consumer_timeout_ms = int(os.getenv('KAFKA_CONSUMER_TIMEOUT_MS'))
    flush_interval = int(os.getenv('KAFKA_FLUSH_INTERVAL'))
    batch_size = int(os.getenv('KAFKA_BATCH_SIZE'))
    kafka_broker_url = os.getenv('KAFKA_BROKER_URL')
    last_flush_time = time.time()
    table_ddl = '''CREATE TABLE IF NOT EXISTS default.clickstream_data (
                user_id String,
                item_id String, 
                interaction_type String,
                timestamp String
            )
            ENGINE = MergeTree()
            ORDER BY (user_id, timestamp)'''
    table_name = 'default.clickstream_data'

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
                        flush_to_clickhouse(pd.DataFrame(data),table_ddl,table_name)
                        message_count = 0
                        data = []
                        last_flush_time = time.time()

                
        else:
            print('No messages received in this poll, retrying')
            print(f'Total messages received: {message_count}')
            retries += 1
            time.sleep(1)
    print(f'Flushing {len(data)} messages to ClickHouse for the final time before closing')
    flush_to_clickhouse(pd.DataFrame(data),table_ddl,table_name)
    
    consumer.close()
    return data 
    
    
def flush_to_clickhouse(data,table_ddl,table_name):
    if len(data.index)>0:
        clickhouse_client = clickhouse_connect.get_client(
            host=os.getenv('CLICKHOUSE_HOST'),
            user=os.getenv('CLICKHOUSE_USER'),
            password=os.getenv('CLICKHOUSE_PASSWORD'),
            secure=True
        )
        clickhouse_client.command(table_ddl)
        clickhouse_client.insert(table_name, data)
        print(f"Inserted {len(data)} rows into ClickHouse")
        


if __name__ == '__main__':
    main()

      