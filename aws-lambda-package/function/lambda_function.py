import json
import psycopg2
import os
from urllib.parse import unquote_plus


def update_db(key,etag,author,title):

    conn = psycopg2.connect(user=os.environ['user'],
                            password=os.environ['password'],
                            host=os.environ['host'],
                            dbname=os.environ['dbname'])
    cur = conn.cursor()
    
    sql_query = """
                UPDATE books
                SET object_key = %s, author = %s, title = %s
                WHERE e_tag = %s
                """
    
    cur.execute(sql_query,(key,author,title,etag))
    conn.commit()
    conn.close()


def clean_up_event_data(event_data):
    etag = '"' + event_data["eTag"] + '"'
    key = unquote_plus(event_data["key"])
    path, title = os.path.split(key)
    author = path
    if "/" in path:
        author = path[0: path.find("/")]
    
    return key,etag,author,title

def lambda_handler(event, context):
    print(event)

    event_data = event["Records"][0]["s3"]["object"]
    key,etag,author,title = clean_up_event_data(event_data)
    update_db(key,etag,author,title)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
