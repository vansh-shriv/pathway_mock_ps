import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import joblib
import sys

def create_features(df, lags=5):
    df_feat = df.copy().reset_index(drop=True)
    df_feat['close'] = df_feat['close'].astype(float)

    # lag features: close_{t-1}, close_{t-2}, ...
    for lag in range(1, lags + 1):
        df_feat[f'lag_{lag}'] = df_feat['close'].shift(lag)

    # percentage change and simple moving averages (based on past)
    df_feat['ret_1'] = df_feat['close'].pct_change(periods=1)
    df_feat['ma_short'] = df_feat['close'].rolling(window=min(3, lags)).mean().shift(1)
    df_feat['ma_medium'] = df_feat['close'].rolling(window=min(7, lags * 2)).mean().shift(1)
    df_feat['vol_rolling'] = df_feat['volume'].rolling(window=min(7, lags * 2)).mean().shift(1)

    # target (next timestamp's close)
    df_feat['target_next'] = df_feat['close'].shift(-1)

    # drop NaN rows from rolling/shift
    df_feat = df_feat.dropna().reset_index(drop=True)
    return df_feat


def directional_accuracy(current_close, predicted_next, actual_next):
    pred_dir = np.sign(predicted_next - current_close)
    actual_dir = np.sign(actual_next - current_close)
    correct = (pred_dir == actual_dir).astype(int)
    return correct.mean(), correct.sum(), len(correct)


def main(args):
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        sys.exit(2)

    # CoinMarketCap CSV uses ; as delimiter
    df = pd.read_csv(data_path, sep=';')

    # Choose a date column to sort chronologically
    date_col = None
    for c in ['timeOpen', 'timestamp', 'timeClose']:
        if c in df.columns:
            date_col = c
            break

    if not date_col:
        print("No date column found (expected 'timeOpen' or 'timestamp').")
        sys.exit(2)

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)

    required = ['close', 'volume']
    for col in required:
        if col not in df.columns:
            print(f"Missing required column '{col}' in CSV.")
            sys.exit(2)

    # Create features
    df_feat = create_features(df, lags=args.lags)

    feature_cols = [c for c in df_feat.columns if c.startswith('lag_')] + [
        'ret_1', 'ma_short', 'ma_medium', 'vol_rolling'
    ]
    X = df_feat[feature_cols].values
    y = df_feat['target_next'].values

    # Time-based train-test split
    n = len(df_feat)
    test_n = int(np.floor(args.test_size * n))
    train_n = n - test_n
    X_train, X_test = X[:train_n], X[train_n:]
    y_train, y_test = y[:train_n], y[train_n:]

    current_close_test = df_feat['close'].values[train_n:train_n + len(y_test)]

    # Train model
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1))
    ])

    print("Training model...")
    model.fit(X_train, y_train)
    print("Training complete.")

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    acc, correct, total = directional_accuracy(current_close_test, y_pred, y_test)
    acc_pct = acc * 100

    print(f"\nTest Results:")
    print(f"RMSE: {rmse:.4f}")
    print(f"Directional Accuracy: {acc_pct:.2f}% ({correct}/{total})")

    # Plot predicted vs actual
    test_dates = df_feat[date_col].values[train_n:train_n + len(y_test)]
    plt.figure(figsize=(12, 6))
    plt.plot(test_dates, y_test, label='Actual Close', linewidth=1.5)
    plt.plot(test_dates, y_pred, label='Predicted Close', linestyle='--', linewidth=1.5)
    plt.title(f"Predicted vs Actual Close (Acc: {acc_pct:.2f}%)")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out_plot = args.plot or "pred_vs_actual.png"
    plt.savefig(out_plot, dpi=150)
    print(f"Plot saved to: {out_plot}")

    if args.save_model:
        joblib.dump(model, args.save_model)
        print(f"Model saved to: {args.save_model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to semicolon-delimited CSV file")
    parser.add_argument("--lags", type=int, default=5, help="Number of lag features")
    parser.add_argument("--test-size", type=float, default=0.2, help="Fraction of data used for testing")
    parser.add_argument("--plot", type=str, default=None, help="Output plot file name")
    parser.add_argument("--save-model", type=str, default=None, help="Save model file path")
    args = parser.parse_args()
    main(args)
