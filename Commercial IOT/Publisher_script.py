import json
import time
from datetime import datetime
import random
import uuid
from pulsar import Client, AuthenticationToken
from dotenv import load_dotenv
import os

#
# Load environment variables from .env file
load_dotenv()

# Astra Streaming connection details
service_url = os.getenv('DATAGENSERVICE_URL')
auth_token = os.getenv('DATAGENAUTH_TOKEN')
topic_name = os.getenv('DATAGENTOPIC_NAME')

# Create a Pulsar client
client = Client(service_url, authentication=AuthenticationToken(auth_token))

# Create a producer
producer = client.create_producer(topic_name)

def generate_iot_data():
    """Generates simulated IoT data matching the target schema."""
    current_time = datetime.utcnow()
    return {
        "enterprise_uid": f"enterprise_{random.randint(1, 100)}",
        "time_bucket": current_time.replace(minute=0, second=0, microsecond=0).isoformat() + "Z",
        "src_uid": f"sensor_{random.randint(1, 100)}",
        "event_ts": current_time.isoformat() + "Z",
        "qod": random.randint(1, 100),
        "log_uuid": str(uuid.uuid1()),
        "tag_val_d": random.uniform(0, 100),
        "tag_val_t": f"tag_{random.randint(1, 1000)}",
        "uom": "Celsius"
    }

try:
    while True:
        # Generate data and send it
        data = generate_iot_data()
        producer.send(json.dumps(data).encode('utf-8'))
        print(f"Sent data: {data}")

        # Wait for a bit before sending the next set of data
        time.sleep(1)  # Sends data every second
except KeyboardInterrupt:
    print("Stopped data generation")

client.close()
