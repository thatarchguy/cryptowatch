"""Bitcoin tools for application."""

import requests
import redis
import functools

import gdax
from cryptowatch.config import redis_server


rediscon = redis.StrictRedis(host=redis_server, db=0)


@functools.lru_cache(maxsize=128, typed=False)
def BTC_price():
    """
    Grab BTC price from GDAX Exchange.

    :returns: price of BTC
    :rtype: float
    """
    client = gdax.PublicClient()
    value = client.get_product_ticker(product_id='BTC-USD').get('price')
    return round(float(value), 2)


def BTC_to_USD(satoshi):
    """
    Convert BTC to USD.

    :param satoshi: Smallest unit of measurement for BTC
    :type satoshi: int
    :returns: price of given BTC
    :rtype: float
    """
    price = BTC_price()
    btc = satoshi * .00000001
    return round(btc * price, 2)


def check_BTC_wallet(wallet_id):
    """
    Check wallet for any new TXs.

    :param wallet_id: wallet_id to check
    :type wallet_id: str
    :returns: list of formatted messages for new TXs
    :rtype: list
    """
    messages = []
    r = requests.get('https://blockchain.info/rawaddr/{0}'.format(wallet_id))
    if not r.ok:
        raise Exception('Error checking wallet')
    txs = r.json().get('txs')
    for tx in txs:
        # if rediscon.setnx(tx.get('hash'), tx):
            # TX we've never seen
        messages.append(format_BTC_message(wallet_id, tx))
    return messages


def format_BTC_message(wallet_id, tx):
    """
    Format the message for SNS.

    :param wallet_id: wallet_id to check
    :type wallet_id: str
    :param tx: json formatted tx from blockchain.info
    :type tx: json
    :return message: formatted message for SNS
    :rtype: str
    """
    # check if this is a withdrawal by looking at inputs
    satoshi = 0
    for inputs in tx.get('inputs'):
        if inputs.get('prev_out', {}).get('addr') == wallet_id:
            # It's a withdrawal
            satoshi += inputs.get('prev_out').get('value')

    if satoshi > 0:
        # It's a withdrawal
        addresses_to = [outs.get('addr') for outs in tx.get('out')]
        data = {
            'addresses_to': addresses_to,
            'address_from': wallet_id,
            'tx_hash': tx.get('hash'),
            'satoshi': satoshi,
            'btc': (satoshi * .00000001),
            'val_btc': BTC_to_USD(satoshi),
            'unix_time': tx.get('time')
        }
        message = "Sent {0} BTC (${1}) from {2}! https://blockchain.info/tx/{3}".format(
            data.get('btc'), data.get('val_btc'), data.get('address_from'), data.get('tx_hash'))
    else:
        # It's a deposit
        for out in tx.get('out', {}):
            if out.get('addr') == wallet_id:
                satoshi = out.get('value')
        from_addresses = [inputs.get('prev_out', {}).get('addr') for inputs in tx.get('inputs')]
        data = {
            'address_to': wallet_id,
            'addresses_from': '|'.join(from_addresses),
            'tx_hash': tx.get('hash'),
            'satoshi': satoshi,
            'btc': (satoshi * .00000001),
            'val_btc': BTC_to_USD(satoshi),
            'unix_time': tx.get('time')
        }
        message = "Received {0} BTC (${1}) at {2}! https://blockchain.info/tx/{3}".format(
            data.get('btc'), data.get('val_btc'), data.get('address_to'), data.get('tx_hash'))
    return message
