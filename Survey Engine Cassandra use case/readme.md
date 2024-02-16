NoSQLBench is an open-source, benchmarking and testing tool designed for testing and measuring the performance of NoSQL databases/Cassandra under various workloads and scenarios.

Instructions to download and set up NoSQLBench can be found here - https://github.com/nosqlbench/nosqlbench/blob/main/DOWNLOADS.md

The fatest way to get started is to set it up on a local machine directly.

Once nosqlbench is setup, please see the 3 files below along with their descriptions:

1) 'surveyusecase.yaml' - This file contains all the YAML configuration needed to create all the schemas from Voldemort as CQL schemas.

It also includes the insert scripts that insert the data into Cassandra. At this point, sample data based on binding configuration defined in the
YAML file has been inserted for schema testing. It also contains a few sample queries that can be executed on Cassandra based on the data model
that was mapped from Voldemort to Cassandra.

2) 'nosqlbench_commands' - contains the nosqlbench command that needs to be executed on the YAML file. Please create a folder called 'workloads' under the
'nb' folder that gets created after installing nosqlbench and place the YAML file named 'surveyusecase.yaml' under the workloads folder.

If needed, also add parameters username and password to the command here and set values for them.

3) 'Voldemort to CQL query mapping' - this file contains the mapping between Voldemort to Cassandra where the CQL equivalent can be found for all the
queries that are not present in the 'surveyusecase.yaml' file. 
