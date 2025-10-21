# Real-Time AI-Driven Stock/Crypto Price Prediction

## Objective

Develop a toy AI-based program to predict stock or cryptocurrency price movement using historical data. The program predicts the next timestamp's price based solely on past data and evaluates directional accuracy.

## Dataset

* Sample dataset: CoinMarketCap historical data for Bitcoin ["https://coinmarketcap.com/currencies/bitcoin/historical-data/"]
* CSV format example:

```
timeOpen;timeClose;timeHigh;timeLow;name;open;high;low;close;volume;marketCap;circulatingSupply;timestamp
"2025-10-20T00:00:00.000Z";"2025-10-20T23:59:59.999Z";"2025-10-20T15:53:00.000Z";"2025-10-20T00:34:00.000Z";"2781";108667.44;111711.03;107485.01;110588.93;63507793084.59;2204868785654.89;19937518;"2025-10-20T23:59:59.999Z"
```

* Delimiter: `;`

## Approach

1. **Feature Engineering**:

   * Lag features: previous `n` timestamps' close prices
   * Returns: percentage change from previous timestamp
   * Rolling indicators: moving averages (short & medium), rolling volume average

2. **Train-Test Split**:

   * Chronological split (no shuffling) to avoid peeking into the future
   * Test fraction configurable (e.g., 20% of data)

3. **Model**:

   * Random Forest Regressor
   * Pipeline with `StandardScaler` for feature normalization

4. **Prediction & Evaluation**:

   * Predict next timestamp's price based on past features
   * Compute directional accuracy (% of times model correctly predicts up/down)
   * Compute RMSE for regression performance

5. **Visualization**:

   * Plot predicted vs actual close prices
   * Save figure for submission

## How to Run Locally

1. Place your CSV file (e.g., `data.csv`) in the project folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the prediction script:

```bash
python stock_predict.py --data bitcoin_data.csv --lags 5 --test-size 0.2 --plot pred_vs_actual.png
```

4. Output:

   * Terminal: RMSE and directional accuracy
   * File: `pred_vs_actual.png` showing predicted vs actual prices

## Docker Setup

* Dockerfile included to run script in a Linux container:

```bash
docker build -t stock-predict .
docker run --rm -v "$(pwd):/app" stock-predict
```

* This ensures reproducible environment on Windows or Linux.

## Deliverables

* `stock_predict.py` : main prediction script
* `requirements.txt` : Python dependencies
* `Dockerfile` : container setup
* `pred_vs_actual.png` : plot output
* This README.md : explanation of workflow

## Notes

* Ensure model never uses future data for prediction.
* Lags, rolling windows, and test fraction can be adjusted for experimentation.
* Accuracy can be improved by adding more features (technical indicators, EMA, RSI, Bollinger Bands) or using Gradient Boosting models.
* Direct classification of up/down movement may increase directional accuracy compared to regression.

---
