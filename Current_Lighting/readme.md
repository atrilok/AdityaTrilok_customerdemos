# What does each file do
Publisher_script.py - the script required to publish data continuosly based on the schema for the table named 'event_log'. 

schema - event_log - File that has the schema of the main table named 'event_log'

schema_mapping.json - Example of a sample message that is ingested to Astra DB and help on the Astra Streaming topic

Other scripts are optional as we prefer to use the sink connector rather than writing code to ingest data