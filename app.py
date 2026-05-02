from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(title="WeatherSphere")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CITIES = [
    {"name":"Tokyo","country":"Japan","temp":22,"feels":21,"humidity":65,"wind":12,"condition":"Partly Cloudy","icon":"⛅","high":25,"low":18,"pressure":1013,"visibility":10,"uv":6,"aqi":42},
    {"name":"New York","country":"USA","temp":18,"feels":16,"humidity":72,"wind":18,"condition":"Rainy","icon":"🌧️","high":20,"low":14,"pressure":1008,"visibility":6,"uv":3,"aqi":58},
    {"name":"London","country":"UK","temp":14,"feels":12,"humidity":80,"wind":22,"condition":"Overcast","icon":"☁️","high":16,"low":10,"pressure":1005,"visibility":8,"uv":2,"aqi":35},
    {"name":"Sydney","country":"Australia","temp":26,"feels":27,"humidity":55,"wind":15,"condition":"Sunny","icon":"☀️","high":29,"low":21,"pressure":1018,"visibility":15,"uv":9,"aqi":28},
    {"name":"Dubai","country":"UAE","temp":38,"feels":42,"humidity":30,"wind":8,"condition":"Hot & Clear","icon":"🌞","high":42,"low":32,"pressure":1010,"visibility":12,"uv":11,"aqi":75},
    {"name":"Singapore","country":"Singapore","temp":30,"feels":34,"humidity":85,"wind":6,"condition":"Thunderstorm","icon":"⛈️","high":32,"low":26,"pressure":1009,"visibility":5,"uv":8,"aqi":52},
]

FORECAST = [
    {"day":"Mon","icon":"☀️","high":28,"low":20,"rain":5},
    {"day":"Tue","icon":"⛅","high":26,"low":19,"rain":15},
    {"day":"Wed","icon":"🌧️","high":22,"low":17,"rain":70},
    {"day":"Thu","icon":"⛈️","high":20,"low":16,"rain":85},
    {"day":"Fri","icon":"☁️","high":23,"low":18,"rain":30},
    {"day":"Sat","icon":"⛅","high":25,"low":19,"rain":20},
    {"day":"Sun","icon":"☀️","high":27,"low":21,"rain":5},
]

ALERTS = [
    {"level":"warning","title":"Heat Wave Advisory","desc":"Temperatures expected to exceed 40C in Dubai region","time":"2 hours ago"},
    {"level":"danger","title":"Severe Thunderstorm","desc":"Heavy rainfall and lightning expected in Singapore","time":"30 min ago"},
    {"level":"info","title":"Air Quality Alert","desc":"Moderate AQI levels in New York, sensitive groups advised","time":"1 hour ago"},
]

AGENTS = [
    {"name":"Weather Predictor","model":"MiMo V2.5 Pro","status":"active","runs":"2,340","tokens":"14.2M","desc":"Forecasts weather patterns using ensemble models and satellite imagery"},
    {"name":"Alert Classifier","model":"MiMo V2.5","status":"active","runs":"1,560","tokens":"6.8M","desc":"Classifies and prioritizes severe weather alerts by impact severity"},
    {"name":"Climate Analyst","model":"MiMo V2.5 Pro","status":"idle","runs":"890","tokens":"8.4M","desc":"Analyzes long-term climate trends and seasonal patterns"},
    {"name":"AQI Monitor","model":"MiMo V2.5","status":"active","runs":"1,780","tokens":"5.1M","desc":"Tracks air quality indices and provides health recommendations"},
]

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "cities": CITIES, "forecast": FORECAST, "alerts": ALERTS, "agents": AGENTS})

@app.get("/city/{name}", response_class=HTMLResponse)
async def city_detail(request: Request, name: str):
    city = next((c for c in CITIES if c["name"].lower() == name.lower()), None)
    if not city:
        return HTMLResponse("Not found", status_code=404)
    return templates.TemplateResponse("city.html", {"request": request, "city": city, "forecast": FORECAST, "agents": AGENTS})

@app.get("/alerts", response_class=HTMLResponse)
async def alerts_page(request: Request):
    return templates.TemplateResponse("alerts.html", {"request": request, "alerts": ALERTS, "agents": AGENTS})

@app.get("/agents", response_class=HTMLResponse)
async def agents_page(request: Request):
    return templates.TemplateResponse("agents.html", {"request": request, "agents": AGENTS})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6400)
