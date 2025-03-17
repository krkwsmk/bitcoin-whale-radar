<<<<<<< HEAD
# bitcoin-whale-radar
Tracking the Ocean's Largest Movements
=======
# Large Bitcoin Transactions Tracker

This web application displays the largest Bitcoin transactions from recent blocks.

## Setup

1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python app.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## Features

- Displays the top 10 largest Bitcoin transactions from recent blocks
- Shows transactions larger than 10 BTC
- Auto-refreshes every 2 minutes
- Shows transaction details including:
  - Amount in BTC
  - Number of inputs and outputs
  - Transaction timestamp
  - Transaction fee
  - Link to view the transaction on blockchain.info
- Manual refresh button
- Responsive design that works on both desktop and mobile devices

## Technical Details

The application uses the free Blockchain.com API to:
1. Fetch recent blocks
2. Get detailed transaction data from each block
3. Filter and sort transactions by amount
4. Display the largest transactions in a user-friendly interface
>>>>>>> 599a3c0 (first commit)
