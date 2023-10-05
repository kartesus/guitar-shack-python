import http.client
import json
import sys
from datetime import datetime, timedelta
from urllib.parse import urlencode

if __name__ == "__main__":
    product_id = int(sys.argv[1])
    quantity = int(sys.argv[2])

    base_url = "localhost:8000"
    params = {"id": product_id}
    param_string = "?" + urlencode(params)

    conn = http.client.HTTPConnection(base_url)
    conn.request("GET", f"/guitars{param_string}")
    response = conn.getresponse()
    result = json.loads(response.read().decode())

    product = result[0]

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    date_format = "%Y-%m-%d"

    params1 = {
        "product_id": product["product_id"],
        "start_date": start_date.strftime(date_format),
        "end_date": end_date.strftime(date_format),
    }

    param_string1 = "?" + urlencode(params1)

    conn1 = http.client.HTTPConnection("localhost:8000")
    conn1.request("GET", f"/sales{param_string1}")
    response1 = conn1.getresponse()
    result1 = json.loads(response1.read().decode())

    sales = result1
    total = sum(sale["quantity"] for sale in sales)

    if product["stock"] - quantity <= int((total / 30) * product["lead_time"]):
        print(
            f"""
                You need to reorder product {product['product_id']}. 
                Only {product['stock'] - quantity} remaining in stock.
                Restock quantity: {int((total / 30) * product['lead_time'])}
                """
        )
