import requests
import os
TOKEN = os.getenv("8745996247:AAEcisO67tU5_OE0_CjK35FcNZXLoFor0GM")


CHAT_ID = "6753532700"

coins = ["BTC-USD", "ETH-USD"]

prices = {coin: [] for coin in coins}
last_signal = {coin: None for coin in coins}
buy_price = {coin: None for coin in coins}
profit = {coin: 0 for coin in coins}

while True:
    try:
        for coin in coins:
            url = f"https://api.coinbase.com/v2/prices/{coin}/spot"
            response = requests.get(url)
            data = response.json()
            current_price = float(data["data"]["amount"])

            print(f"{coin} ár:", current_price)

            prices[coin].append(current_price)

            if len(prices[coin]) > 20:
                prices[coin].pop(0)

            if len(prices[coin]) >= 5:
                avg = sum(prices[coin]) / len(prices[coin])

                buy_threshold = avg * 0.99
                sell_threshold = avg * 1.01

                print(f"{coin} átlag:", avg)

                # VÉTEL
                if current_price < buy_threshold and last_signal[coin] != "BUY":
                    last_signal[coin] = "BUY"
                    buy_price[coin] = current_price

                    msg = f"🟢 {coin} VÉTEL\nÁr: {current_price}"
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={"chat_id": CHAT_ID, "text": msg}
                    )

                # ELADÁS
                elif current_price > sell_threshold and last_signal[coin] != "SELL":
                    last_signal[coin] = "SELL"

                    if buy_price[coin] is not None:
                        trade_profit = current_price - buy_price[coin]
                        profit[coin] += trade_profit

                        msg = (
                            f"🔴 {coin} ELADÁS\n"
                            f"Ár: {current_price}\n"
                            f"Profit: {round(trade_profit,2)}\n"
                            f"Összes profit: {round(profit[coin],2)}"
                        )
                    else:
                        msg = f"🔴 {coin} ELADÁS (nincs előző vétel)"

                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={"chat_id": CHAT_ID, "text": msg}
                    )

        time.sleep(60)

    except Exception as e:
        print("Hiba:", e)
        time.sleep(10)
