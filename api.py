import random
from datetime import datetime, timedelta

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()


# Function to generate sales data with gaps and seasonal fluctuations with a favored product
def generate_sales_data_with_bias(
    start_date, end_date, product_ids, price_mapping, favored_product
):
    date_range = pd.date_range(start=start_date, end=end_date)
    data = []

    for date in date_range:
        # Introduce 40% chance of no sales
        if random.random() < 0.4:
            continue

        month = date.month
        if month in [11, 12, 1]:  # Winter (higher sales)
            num_sales = random.randint(3, 7)
        elif month in [6, 7, 8]:  # Summer (lower sales)
            num_sales = random.randint(0, 2)
        else:  # Other months (average sales)
            num_sales = random.randint(0, 5)

        for _ in range(num_sales):
            # Favor product 811
            product = (
                favored_product if random.random() < 0.3 else random.choice(product_ids)
            )
            quantity = random.randint(1, 3)
            price = price_mapping[product]
            time = f"{random.randint(0, 23)}:{random.randint(0, 59)}:{random.randint(0, 59)}"

            data.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "time": time,
                    "product_id": product,
                    "quantity": quantity,
                    "price_charged": price,
                }
            )

    return data


guitars_data = [
    {
        "product_id": 757,
        "make": "Fender",
        "range": "Player",
        "model": "Stratocaster",
        "description": "Fender Player Stratocaster w/ Maple Fretboard in Buttercream",
        "price": 549,
        "stock": 12,
        "rack_space": 20,
        "lead_time": 14,
        "min_order": 10,
    },
    {
        "product_id": 449,
        "make": "Fender",
        "range": "Deluxe",
        "model": "Telecaster",
        "description": "Fender Deluxe Nashville Telecaster MN in 2 Colour Sunburst",
        "price": 769,
        "stock": 5,
        "rack_space": 10,
        "lead_time": 21,
        "min_order": 5,
    },
    {
        "product_id": 374,
        "make": "Ibanez",
        "range": "Prestige",
        "model": "RG652AHMFX-NGB",
        "description": "Ibanez RG652AHMFX-NGB RG Prestige Nebula Green Burst (inc. case)",
        "price": 1199,
        "stock": 2,
        "rack_space": 5,
        "lead_time": 60,
        "min_order": 1,
    },
    {
        "product_id": 811,
        "make": "Epiphone",
        "range": "Les Paul",
        "model": "Les Paul Classic",
        "description": "Epiphone Les Paul Classic In Worn Heritage Cherry Sunburst",
        "price": 399,
        "stock": 22,
        "rack_space": 30,
        "lead_time": 14,
        "min_order": 20,
    },
]


def extract_product_info(guitars_data):
    product_ids = [guitar["product_id"] for guitar in guitars_data]
    price_mapping = {guitar["product_id"]: guitar["price"] for guitar in guitars_data}
    return product_ids, price_mapping


def get_date_range():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14 * 30)  # Approximate 14 months
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


start_date, end_date = get_date_range()
product_ids, price_mapping = extract_product_info(guitars_data)
sales_data = generate_sales_data_with_bias(
    start_date, end_date, product_ids, price_mapping, 811
)


@app.get("/guitars")
async def get_guitars(id: int = Query(None)):
    if id:
        return JSONResponse(
            content=[guitar for guitar in guitars_data if guitar["product_id"] == id]
        )
    return JSONResponse(content=guitars_data)


@app.get("/sales")
async def get_sales(
    product_id: int = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    filtered_sales = sales_data
    if product_id:
        filtered_sales = [
            sale for sale in filtered_sales if sale["product_id"] == product_id
        ]
    if start_date:
        filtered_sales = [sale for sale in filtered_sales if sale["date"] >= start_date]
    if end_date:
        filtered_sales = [sale for sale in filtered_sales if sale["date"] <= end_date]
    return JSONResponse(content=filtered_sales)
