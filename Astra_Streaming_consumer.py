from pulsar import Client, AuthenticationToken, ConsumerType
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Astra Streaming connection details
service_url = os.getenv('DATAGENSERVICE_URL')
auth_token = os.getenv('DATAGENAUTH_TOKEN')
topic_name = os.getenv('DATAGENTOPIC_NAME')

# Create a Pulsar client
client = Client(service_url, authentication=AuthenticationToken(auth_token))

# Create a consumer
consumer = client.subscribe(topic_name, subscription_name="my-subscription", consumer_type=ConsumerType.Shared)

try:
    while True:
        # Receive messages from the topic
        msg = consumer.receive()
        try:
            # Deserialize the message content
            data = json.loads(msg.data())
            print(f"Received data: {data}")

            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)

        except Exception as e:
            print(f"Failed to process message: {str(e)}")
            # Negative acknowledgement in case of processing failure
            consumer.negative_acknowledge(msg)

except KeyboardInterrupt:
    print("Stopped data subscription")

client.close()
