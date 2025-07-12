# crm/cron_jobs/send_order_reminders.py

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Setup logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# GraphQL setup
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
client = Client(transport=transport, fetch_schema_from_transport=False)

# Date filter
today = datetime.now()
seven_days_ago = today - timedelta(days=7)
date_from = seven_days_ago.strftime("%Y-%m-%d")

# GraphQL query
query = gql("""
query GetRecentOrders($from: Date!) {
  orders(orderDate_Gte: $from, status: "PENDING") {
    id
    customer {
      email
    }
  }
}
""")

# Run query
params = {"from": date_from}
try:
    result = client.execute(query, variable_values=params)
    for order in result["orders"]:
        log_entry = f"{datetime.now()} - Order ID: {order['id']}, Email: {order['customer']['email']}"
        logging.info(log_entry)
except Exception as e:
    logging.error(f"{datetime.now()} - Error fetching orders: {e}")

print("Order reminders processed!")
