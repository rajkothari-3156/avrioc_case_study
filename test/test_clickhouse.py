import clickhouse_connect
import os

if __name__ == '__main__':
    client = clickhouse_connect.get_client(
        host=os.getenv('CLICKHOUSE_HOST'),
        user=os.getenv('CLICKHOUSE_USER'),
        password=os.getenv('CLICKHOUSE_PASSWORD'),
        secure=True
    )
    print("Result:", client.query("SELECT * from default.noaa_enriched limit 10").result_set)