import os
import json
import requests
from elasticsearch import Elasticsearch  # type: ignore

# Configuration
ELASTICSEARCH_HOST = "http://localhost:9200"
GRAFANA_API_URL = "http://localhost:3000/api/dashboards/db"
GRAFANA_API_KEY = "grafana_api_key"
DASHBOARD_CONFIG_FOLDER = "./dashboard_config"
DASHBOARD_FOLDER = "./grafana_dashboards"

es = Elasticsearch(ELASTICSEARCH_HOST)

# Load dashboard configurations
dashboard_files = [f for f in os.listdir(DASHBOARD_CONFIG_FOLDER) if f.endswith(".json")]
dashboards = []

for file_name in dashboard_files:
    with open(os.path.join(DASHBOARD_CONFIG_FOLDER, file_name), "r") as file:
        try:
            dashboard = json.load(file)
            dashboards.append(dashboard)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON file: {file_name}")

#prompt user to implement all or selected dashboards
print("Select an option:")
print("1. Implement all dashboards")
print("2. Select specific dashboards")

option = input("Enter the number corresponding to your choice: ")

if option == "1":
    selected_dashboards = dashboards
elif option == "2":
    print("Available dashboards:")
    for idx, dashboard in enumerate(dashboards, 1):
        print(f"{idx}. {dashboard['name']}")

    selected = input("Enter the numbers of dashboards to implement (comma-separated): ")
    selected_indices = [int(i.strip()) - 1 for i in selected.split(",")]
    selected_dashboards = [dashboards[i] for i in selected_indices]
else:
    print("Invalid option. Exiting.")
    exit()

def create_dashboard(dashboard_config):
    dashboard_payload = {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": dashboard_config["name"],
            "tags": ["monitoring"],
            "timezone": "browser",
            "panels": []
        },
        "overwrite": True
    }

    for panel in dashboard_config["panels"]:
        panel_data = {
            "title": panel["title"],
            "type": panel["type"],
            "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
            "targets": [
                {
                    "refId": "A",
                    "format": "time_series",
                    "datasource": "Elasticsearch",
                    "metricName": panel["metric"],
                    "aggregation": panel["agg"]
                }
            ],
        }
        dashboard_payload["dashboard"]["panels"].append(panel_data)

    dashboard_file = os.path.join(DASHBOARD_FOLDER, f"{dashboard_config['name']}.json")
    with open(dashboard_file, "w") as file:
        json.dump(dashboard_payload, file, indent=4)

    return dashboard_file

for dashboard_config in selected_dashboards:
    dashboard_file = create_dashboard(dashboard_config)
    print(f"Dashboard JSON saved to: {dashboard_file}")

    with open(dashboard_file, "r") as file:
        dashboard_payload = json.load(file)

    headers = {
        "Authorization": f"Bearer {GRAFANA_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(GRAFANA_API_URL, json=dashboard_payload, headers=headers)

    if response.status_code == 200:
        print(f"Dashboard '{dashboard_config['name']}' created successfully!")
    else:
        print(f"Failed to create dashboard '{dashboard_config['name']}': {response.status_code}")
        print(response.text)
