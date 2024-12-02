# grafana-dashboard

To create Grafana dashboard using python

Assuming there are services which has multiple microservices deployed on EC2 instances with database which requires monitoring setup.

The first set of monitoring dashboards required could be as follows:

EC2 Instances:
 Instance state
 CPU utilization, memory usage, disk I/O, network traffic (in/out)

 Average uptime

Database:
 CPU/memory utilization of the database server
 Query performance and execution time
 Connections and session counts
 Disk space

Centralized Logging:
 Logs of all services and microservices

Assumption:

Metrics of EC2 instances are present in elasticsearch
Grafana endpoint is available on localhost

List of available dashboards:
    "Infrastructure Monitoring (CPU Utilization, Instance Health)",
    "Log Analytics",
    "Database Monitoring",
    "Health and Availability"

To run:
 python grafana_dashboards.py
