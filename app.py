from flask import Flask, render_template, request

app = Flask(__name__)

# Currency conversion rates to EUR (1 unit = X EUR)
EXCHANGE_RATES = {
    'EUR': 1.0,
    'USD': 0.92,
    'GBP': 1.18,
    'JPY': 0.0067,
    'INR': 0.011,
    'AUD': 0.60,
    'CAD': 0.67,
    'CHF': 1.08,
    'CNY': 0.13,
    'SEK': 0.092,
    'SGD': 0.68,
    'HKD': 0.12,
}

@app.route('/')
def index():
    return render_template('index.html', currencies=sorted(EXCHANGE_RATES.keys()))


@app.route('/results')
def results():
    electricity = float(request.args.get('electricity', 0))
    electricity_currency = request.args.get('electricity_currency', 'EUR')
    
    gas = float(request.args.get('gas', 0))
    gas_currency = request.args.get('gas_currency', 'EUR')
    
    car = float(request.args.get('car', 0))
    flights = float(request.args.get('flights', 0))

    # Convert to EUR for calculation
    electricity_eur = electricity * EXCHANGE_RATES.get(electricity_currency, 1.0)
    gas_eur = gas * EXCHANGE_RATES.get(gas_currency, 1.0)

    # Calculate footprints (emission factors based on EUR)
    electricityFootprint = electricity_eur * 0.5  # kgCO2e per €
    gasFootprint = gas_eur * 0.2
    carFootprint = car * 0.12
    flightFootprint = flights * 250

    totalFootprint = electricityFootprint + gasFootprint + carFootprint + flightFootprint

    return render_template('results.html', e=electricityFootprint, g=gasFootprint, c=carFootprint, f=flightFootprint, total=totalFootprint, 
                         electricity_currency=electricity_currency, gas_currency=gas_currency)

if __name__ == '__main__':
    app.run(debug=True)
