def predict_prices(village_data, weather_data, busy_data):
    import random
    import json 
    #load json filter_result.json
    with open('filtered_comparison_results.json') as f:
        data = json.load(f)
    # Mock ML logic
    temp = weather_data["temperature"]
    print("temp", temp) 
    print(weather_data)
    is_bad_weather = "rain" in weather_data["condition"].lower() or temp < 45.0
    is_busy = busy_data.get("busy_level", 0) > 70  # Mock busy threshold
    print("is_bad_weather", is_bad_weather)
    print("is_busy", is_busy)
    predicted_prices = []
    for item in village_data["menu"]:
        for d in data:
            if d['main_dish'] == item['name']:
                item['price'] = d['nearby_price']
                break
        if type(item['price']) == str:
            base_price = float(item["price"].replace("$", ""))
        else:
            base_price= float(item["price"])
        if is_bad_weather or is_busy:
            price = base_price * random.uniform(1.2, 1.5)  # Increase by 20-50%
        else:
            price = base_price
        predicted_prices.append(
                {"item": item["name"], "price": round(price, 2)})

    return predicted_prices
