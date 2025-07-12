from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Write log
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional: GraphQL hello check
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("""query { hello }""")
        result = client.execute(query)
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL error: {e}\n")

def update_low_stock():
    mutation = gql("""
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    """)

    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        result = client.execute(mutation)

        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        log_lines = [f"{timestamp} - {p['name']} restocked to {p['stock']}" for p in result["updateLowStockProducts"]["updatedProducts"]]

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for line in log_lines:
                f.write(line + "\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{datetime.now()} - Error: {e}\n")