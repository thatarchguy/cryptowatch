"""Ethereum tools for application."""

import functools

import gdax
import requests
import redis

from cryptowatch.config import redis_server

rediscon = redis.StrictRedis(host=redis_server, db=0)


@functools.lru_cache(maxsize=128, typed=False)
def ETH_price():
    """
    Grab ETH price from GDAX Exchange.

    :returns: price of ETH
    :rtype: float
    """
    client = gdax.PublicClient()
    value = client.get_product_ticker(product_id='ETH-USD').get('price')
    return round(float(value), 2)


def ETH_to_USD(wei):
    """
    Convert ETH to USD.

    :param wei: Smallest unit of Ethereum
    :type wei: int
    :returns: price of given ETH
    :rtype: float
    """
    price = ETH_price()
    eth = wei * .000000000000000001
    return round(eth * price, 2)


def check_ETH_wallet(wallet_id):
    """
    Check wallet for any new TXs.

    :param wallet_id: wallet_id to check
    :type wallet_id: str
    :returns: list of formatted messages for new TXs
    :rtype: list
    """
    messages = []
    r = requests.get(
        'https://api.etherscan.io/api?module=account&action=txlist&address={0}'.format(wallet_id))
    if not r.ok:
        raise Exception('Error checking wallet')
    txs = r.json().get('result')
    for tx in txs:
        # if rediscon.setnx(tx.get('hash'), tx):
            # TX we've never seen
        messages.append(format_ETH_message(wallet_id, tx))
    return messages


def format_ETH_message(wallet_id, tx):
    """
    Format the message for SNS.

    :param wallet_id: wallet_id to check
    :type wallet_id: str
    :param tx: json formatted tx from api.etherscan.io
    :type tx: json
    :return message: formatted message for SNS
    :rtype: str
    """
    wei = int(tx.get('value'))
    data = {
        'withdrawal': None,
        'address_to': None,
        'address_from': None,
        'tx_hash': tx.get('hash'),
        'wei': wei,
        'eth': (wei * .000000000000000001),
        'val_eth': ETH_to_USD(wei),
        'unix_time': tx.get('time')
    }
    if tx.get('from') == wallet_id:
        # It's a withdrawal
        data['withdrawal'] = True
        data['address_to'] = tx.get('to')
        data['address_from'] = wallet_id

        message = "Sent {0} ETH (${1}) from {2}! https://etherscan.io/tx/{3}".format(
            data.get('eth'), data.get('val_eth'), data.get('address_from'), data.get('tx_hash'))
    elif tx.get('to') == wallet_id:
        # It's a deposit
        data['withdrawal'] = False
        data['address_to'] = wallet_id
        data['address_from'] = tx.get('from')

        message = "Received {0} ETH (${1}) at {2}! https://etherscan.io/tx/{3}".format(
            data.get('eth'), data.get('val_eth'), data.get('address_to'), data.get('tx_hash'))
    else:
        raise Exception("Address not in to or from for transaction...weird")
    return message
