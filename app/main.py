from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from utils.apis import fetch_yelp_data, fetch_weather_data, fetch_busy_times
from models.ml_model import predict_prices
import json

with open('menu_items_village.json') as f:
    menu_items_village = json.load(f)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Step 1: Fetch data
    village_data = menu_items_village
    weather_data = fetch_weather_data()
    busy_data = fetch_busy_times()
    # weather_data={"temperature": 20, "condition": "Sunny"}
    # busy_data={"busy_level": 80}
    # Step 2: Predict prices
    # print("village_data", village_data)
    predicted_prices = predict_prices(village_data, weather_data, busy_data)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "village_data": village_data,
        "weather_data": weather_data,
        "busy_data": busy_data,
        "predicted_prices": predicted_prices
    })
