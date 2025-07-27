from slack_sdk import WebClient
import os
import clickhouse_connect
from datetime import datetime
def monitor_item_sales():
    current_date = str(datetime.now().strftime('%Y-%m-%d'))
    clickhouse_client = clickhouse_connect.get_client(
                host=os.getenv('CLICKHOUSE_HOST'),
                user=os.getenv('CLICKHOUSE_USER'),
                password=os.getenv('CLICKHOUSE_PASSWORD'),
                secure=True
            )

    result =clickhouse_client.query(f'''
        
        select * from
        (SELECT item_id,sum(total_purchases) as total_purchases FROM default.fct_item
        WHERE event_date = '{current_date}'
        group by 1 )
        where  total_purchases > 
                                (Select avg(total_purchases)*1.5 
                                from (select item_id,
                                        sum(total_purchases) as total_purchases
                                from default.fct_item where event_date = '{current_date}'
                                group by 1 ))
        
        order by 2 desc
        
    ''')
    if len(result.result_rows)>0:
        slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        slack_client.chat_postMessage(channel='#everyone', text=f'Item sales are above statistically higher than average for the following items: {result.result_rows}')



if __name__ == '__main__':
    monitor_item_sales()

