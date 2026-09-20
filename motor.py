import yfinance as yf
import json
import time

# Tu Universo de Acciones (Puedes agregar más después)
tickers = ["AAPL", "MSFT", "GOOGL", "JNJ", "PG", "NVDA", "WMT", "KO", "PEP", "V", "JPM", "BAC", "CVX", "MCD"]

datos_finales = []
print("Iniciando la extracción de datos de Wall Street...")

for ticker in tickers:
    try:
        empresa = yf.Ticker(ticker)
        info = empresa.info
        
        nombre = info.get("shortName", ticker)
        sector = info.get("sector", "Desconocido")
        precio = info.get("currentPrice", info.get("regularMarketPrice", 0))
        fair_value = info.get("targetMeanPrice", precio)
        
        roa = info.get("returnOnAssets", 0) * 100 if info.get("returnOnAssets") else 0
        ebitda = info.get("ebitda", 0)
        ev = info.get("enterpriseValue", 0)
        earnings_yield = (ebitda / ev * 100) if ev and ev > 0 else 0
        
        div_yield = info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0
        deuda_equity = info.get("debtToEquity", 0) / 100 if info.get("debtToEquity") else 0
        crecimiento_ventas = info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0
        beta = info.get("beta", 1.0)
        payout_ratio = info.get("payoutRatio", 0) * 100 if info.get("payoutRatio") else 0
        
        f_score = 5
        if roa > 0: f_score += 1
        if crecimiento_ventas > 0: f_score += 1
        if deuda_equity < 1.0: f_score += 1
        if info.get("operatingMargins", 0) > 0.15: f_score += 1
        
        if precio > 0:
            datos_finales.append({
                "ticker": ticker, "nombre": nombre, "sector": sector,
                "precio": round(precio, 2), "fair_value": round(fair_value, 2),
                "f_score": f_score, "roic": round(roa, 2),
                "earnings_yield": round(earnings_yield, 2), "dividend_yield": round(div_yield, 2),
                "deuda_equity": round(deuda_equity, 2), "crecimiento_ventas": round(crecimiento_ventas, 2),
                "beta": round(beta, 2), "payout_ratio": round(payout_ratio, 2)
            })
            print(f"✅ {ticker} extraído.")
        
        time.sleep(1) # Pausa para no saturar a Yahoo
        
    except Exception as e:
        print(f"❌ Error con {ticker}: {e}")

with open("datos_empresas.json", "w", encoding="utf-8") as f:
    json.dump(datos_finales, f, indent=4, ensure_ascii=False)

print("\n¡Éxito! Archivo 'datos_empresas.json' creado.")