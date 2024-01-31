from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from pulsar import Client, AuthenticationToken,ConsumerType
import json
from datetime import datetime
import time
from cassandra.util import uuid_from_time
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Astra DB Config
astra_db_client_id = os.getenv('astra_db_client_id')
astra_db_client_secret = os.getenv('astra_db_client_secret')
astra_db_keyspace = os.getenv('astra_db_keyspace')
astra_db_table = os.getenv('astra_db_table')
astra_db_cloud_config = {'secure_connect_bundle': '/Users/adityatrilok/Documents/Customers/scb/secure-connect-commercial-lighting.zip'}

# Astra Streaming connection details
service_url = os.getenv('SERVICE_URL')
auth_token = os.getenv('AUTH_TOKEN')
topic_name = os.getenv('TOPIC_NAME')

# Setup Astra DB Connection
auth_provider = PlainTextAuthProvider(username=astra_db_client_id, password=astra_db_client_secret)
cluster = Cluster(cloud=astra_db_cloud_config, auth_provider=auth_provider)
session = cluster.connect(astra_db_keyspace)

def create_event_log_table(session):
    """Create the event_log table in the lighting_data keyspace."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS lighting_data.event_log (
        enterprise_uid text,
        time_bucket timestamp,
        src_uid text,
        event_ts timestamp,
        qod int,
        log_uuid timeuuid,
        tag_val_d double,
        tag_val_t text,
        uom text static,
        PRIMARY KEY ((enterprise_uid, time_bucket, src_uid), event_ts, qod, log_uuid)
    );
    """
    session.execute(create_table_query)

# Create the table before starting message consumption
create_event_log_table(session)


# Setup Astra Streaming Consumer
client = Client(service_url, authentication=AuthenticationToken(auth_token))
consumer = client.subscribe(topic_name, subscription_name="my-shared-subscription", consumer_type=ConsumerType.Shared)

def insert_into_astra_db(data, session):
    """Insert data into Astra DB in the lighting_data.event_log table."""
    # Convert ISO 8601 formatted strings to datetime objects
    time_bucket = datetime.fromisoformat(data['time_bucket'].rstrip('Z'))
    event_ts = datetime.fromisoformat(data['event_ts'].rstrip('Z'))

    # Convert datetime objects to timestamps (milliseconds since epoch)
    time_bucket_ts = int(time.mktime(time_bucket.timetuple()) * 1000)
    event_ts_ts = int(time.mktime(event_ts.timetuple()) * 1000)

    # Generate a TimeUUID for log_uuid
    log_uuid_time = datetime.utcnow()
    log_uuid = uuid_from_time(log_uuid_time)

    cql_query = """
        INSERT INTO lighting_data.event_log (enterprise_uid, time_bucket, src_uid, event_ts, qod, log_uuid, tag_val_d, tag_val_t, uom)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(cql_query, (data['enterprise_uid'], time_bucket_ts, data['src_uid'], event_ts_ts, data['qod'], log_uuid, data['tag_val_d'], data['tag_val_t'], data['uom']))


try:
    while True:  # This loop will keep running until the script is interrupted
        msg = consumer.receive(timeout_millis=5000)  # Adjust timeout as needed
        try:
            # Assuming data is the parsed message content
            data = json.loads(msg.data().decode('utf-8'))

            # Call the function with the session argument
            insert_into_astra_db(data, session)

            consumer.acknowledge(msg)
        except Exception as e:
            print(f"Failed to process message: {e}")
            consumer.negative_acknowledge(msg)
except KeyboardInterrupt:
    print("Shutting down consumer...")

# Clean up
client.close()

