from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def format_number(number, format_type='regular'):
    """Format numbers for display"""
    try:
        if format_type == 'price':
            return f"{float(number):,.2f}"
        elif format_type == 'value':
            number = float(number)
            if number >= 1_000_000_000:
                return f"${number / 1_000_000_000:.2f}B"
            elif number >= 1_000_000:
                return f"${number / 1_000_000:.2f}M"
            elif number >= 1_000:
                return f"${number / 1_000:.2f}K"
            return f"${number:.2f}"
        else:  # regular format
            return f"{float(number):,.8f}"
    except (ValueError, TypeError) as e:
        logger.error(f"Error formatting number {number}: {e}")
        return "0.00"

def get_btc_price():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"BTC Price fetched successfully")
            return float(data['price'])
        else:
            logger.error(f"BTC Price API Error: Status code {response.status_code}")
    except Exception as e:
        logger.error(f"Error fetching BTC price: {e}")
    return 65000  # Default fallback price

def get_historical_transactions():
    try:
        # Use a different endpoint that's more reliable
        url = "https://blockchain.info/charts/n-transactions?timespan=30days&format=json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info("Historical transactions fetched successfully")
            values = []
            for point in data.get('values', []):
                try:
                    values.append({
                        'x': int(point['x']),
                        'y': float(point['y'])
                    })
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing data point: {e}")
                    continue
            return values
        else:
            logger.error(f"Historical Transactions API Error: Status code {response.status_code}")
            # Return sample data if API fails
            current_time = int(time.time())
            return [{'x': current_time - (i * 86400), 'y': 300000 - (i * 1000)} for i in range(30)]
    except Exception as e:
        logger.error(f"Error fetching historical transactions: {e}")
        return []

def get_rich_list():
    try:
        # Use blockchair.com API for better reliability
        addresses = [
            "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo",  # Binance Cold Wallet
            "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq4nw842ns4vw0eh",  # Bitfinex Cold Wallet
            "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ",  # Huobi Cold Wallet
            "3LQUu4v9z6KNch71j7kbj8GPeAGUo1FW6a",  # Binance Hot Wallet
            "bc1qa5wkgaew2dkv56kfvj49j0av5nml45x9ek9hz6",  # Unknown Whale
            "1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd",  # Huobi Cold Wallet 2
            "3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS",  # OKX Cold Wallet
            "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s"   # Binance Cold Wallet 2
        ]
        
        rich_list = []
        current_price = get_btc_price()
        
        # Add delay between requests to avoid rate limiting
        for address in addresses:
            try:
                url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
                response = requests.get(url, timeout=10)
                time.sleep(0.5)  # Add delay between requests
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('data'):
                        address_data = data['data'][address]['address']
                        balance_btc = float(address_data['balance']) / 100000000
                        
                        rich_list.append({
                            'address': address,
                            'balance_btc': format_number(balance_btc, 'regular'),
                            'balance_usd': format_number(balance_btc * current_price, 'value')
                        })
                        logger.info(f"Fetched balance for {address}")
                else:
                    # Fallback to blockchain.info if blockchair fails
                    url = f"https://blockchain.info/balance?active={address}"
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        balance_btc = data.get(address, {}).get('final_balance', 0) / 100000000
                        
                        rich_list.append({
                            'address': address,
                            'balance_btc': format_number(balance_btc, 'regular'),
                            'balance_usd': format_number(balance_btc * current_price, 'value')
                        })
                        logger.info(f"Fetched balance for {address} from fallback API")
            except Exception as e:
                logger.error(f"Error fetching rich list for address {address}: {e}")
                continue
                
        return rich_list
    except Exception as e:
        logger.error(f"Error in get_rich_list: {e}")
        return []

def get_satoshi_addresses():
    try:
        satoshi_addresses = [
            {
                "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "description": "Genesis Block Address",
                "block_height": 0,
                "date_mined": "2009-01-03",
                "balance": 50
            },
            {
                "address": "12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX",
                "description": "First Block After Genesis",
                "block_height": 1,
                "date_mined": "2009-01-03",
                "balance": 50
            },
            {
                "address": "1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1",
                "description": "Early Satoshi Block",
                "block_height": 2,
                "date_mined": "2009-01-03",
                "balance": 50
            }
        ]
        
        current_price = get_btc_price()
        for addr in satoshi_addresses:
            addr['balance_usd'] = format_number(addr['balance'] * current_price, 'value')
            addr['balance_btc'] = format_number(addr['balance'], 'regular')
        
        return satoshi_addresses
    except Exception as e:
        logger.error(f"Error processing Satoshi addresses: {e}")
        return []

def get_large_transactions():
    try:
        current_price = get_btc_price()
        
        data = {
            "current_btc_price": format_number(current_price, 'price'),
            "transactions": [],
            "rich_list": get_rich_list(),
            "satoshi_addresses": get_satoshi_addresses(),
            "historical_transactions": get_historical_transactions()
        }
        
        try:
            # Use whale-alert.io API for better transaction data
            url = "https://api.whale-alert.io/v1/transactions?api_key=YOUR_API_KEY&min_value=1000000"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                tx_data = response.json()
                logger.info(f"Fetched whale transactions successfully")
                
                for tx in tx_data.get('transactions', []):
                    try:
                        amount_btc = float(tx['amount'])
                        if amount_btc > 10:  # Only transactions > 10 BTC
                            data['transactions'].append({
                                'hash': tx['hash'],
                                'amount': format_number(amount_btc, 'regular'),
                                'timestamp': tx['timestamp'],
                                'fee': format_number(tx.get('fee', 0), 'regular'),
                                'inputs_count': 1,
                                'outputs_count': 1,
                                'status': 'Confirmed' if tx.get('status') == 'completed' else 'Unconfirmed',
                                'btc_price_usd': format_number(current_price, 'price'),
                                'total_value_usd': format_number(amount_btc * current_price, 'value')
                            })
                    except (KeyError, TypeError) as e:
                        logger.error(f"Error processing whale transaction: {e}")
                        continue
            else:
                # Fallback to blockchain.info if whale-alert fails
                url = "https://blockchain.info/unconfirmed-transactions?format=json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    tx_data = response.json()
                    logger.info(f"Fetched {len(tx_data.get('txs', []))} recent transactions from fallback API")
                    
                    for tx in tx_data.get('txs', []):
                        try:
                            total_output = sum(out['value'] for out in tx['out']) / 100000000
                            
                            if total_output > 10:  # Only transactions > 10 BTC
                                fee = (sum(inp.get('prev_out', {}).get('value', 0) for inp in tx['inputs']) - 
                                      sum(out['value'] for out in tx['out'])) / 100000000
                                
                                data['transactions'].append({
                                    'hash': tx['hash'],
                                    'amount': format_number(total_output, 'regular'),
                                    'timestamp': tx['time'],
                                    'fee': format_number(fee, 'regular'),
                                    'inputs_count': len(tx['inputs']),
                                    'outputs_count': len(tx['out']),
                                    'status': 'Unconfirmed',
                                    'btc_price_usd': format_number(current_price, 'price'),
                                    'total_value_usd': format_number(total_output * current_price, 'value')
                                })
                        except (KeyError, TypeError) as e:
                            logger.error(f"Error processing transaction: {e}")
                            continue
        except Exception as e:
            logger.error(f"Error fetching recent transactions: {e}")
        
        # Sort transactions by amount
        data['transactions'].sort(key=lambda x: float(x['amount'].replace(',', '')), reverse=True)
        data['transactions'] = data['transactions'][:10]
        
        return jsonify(data)
        
    except Exception as e:
        logger.error(f"Error in get_large_transactions: {e}")
        return jsonify({
            "current_btc_price": format_number(current_price, 'price') if current_price else "0.00",
            "transactions": [],
            "rich_list": [],
            "satoshi_addresses": [],
            "historical_transactions": []
        })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return get_large_transactions()

if __name__ == '__main__':
    app.run(debug=True)
