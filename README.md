# Bitcoin Whale Radar 🐋

A real-time dashboard for tracking Bitcoin whale activities, large transactions, and monitoring Satoshi's original wallet addresses. Built with Python Flask and modern web technologies.

![Bitcoin Whale Radar](https://bitcoin.org/img/icons/opengraph.png)

## Features

- 📊 Real-time Bitcoin price tracking
- 🔍 Monitor top Bitcoin whale wallets and their balances
- 💰 Track large Bitcoin transactions
- 🏛️ Historical transaction data visualization
- 🔗 Original Satoshi wallet monitoring
- ⚡ Auto-refreshing data every 2 minutes
- 🎨 Modern, responsive UI with neon cyberpunk theme

## Tech Stack

- Backend: Python Flask
- Frontend: HTML5, CSS3, JavaScript
- Charts: Chart.js
- Styling: Bootstrap 5
- APIs: 
  - Binance (Price data)
  - Blockchain.info
  - Blockchair.com

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jaibhasin/bitcoin-whale-radar.git
cd bitcoin-whale-radar
```

2. Install required Python packages:
```bash
pip install flask requests python-dateutil
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## API Rate Limits

The application respects API rate limits by:
- Implementing 0.5s delay between wallet balance requests
- Refreshing data every 2 minutes instead of every minute
- Using fallback APIs when primary APIs are unavailable

## Contributing

Feel free to fork the project and submit pull requests. You can also open issues for bugs or feature requests.

## License

This project is open source and available under the MIT License.

## Disclaimer

This application is for educational purposes only. Always do your own research before making any investment decisions. Cryptocurrency trading carries significant risks.
