"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?
  You might be tempted to import things from __main__ later,but that will cause
  problems: the code will get executed twice:
  - When you run `python -m cryptowatch` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``cryptowatch.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``cryptowatch.__main__`` in ``sys.modules``.
  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click
# import boto3
import re

from cryptowatch.btc import check_BTC_wallet
from cryptowatch.eth import check_ETH_wallet

# from cryptowatch.config import target_arn

wallets = [{'wallet': '115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn',
            'reason': 'WannaCry Address #1'},
           {'wallet': '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw',
            'reason': 'WannaCry Address #2'},
           {'wallet': '0x64623B1E4250B787568D510611989eCA71D92E1C',
            'reason': 'Some random dude'}]


def determine_wallet_format(wallet_id):
    """
    Check wallet format for given ID.

    :param wallet_id:
    :type wallet_id: wallet_id in some format
    :return: string ("ETH" or "BTC")
    :rtype: string
    :raises: ValueError
    """
    btc_regex = re.compile('^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')
    eth_regex = re.compile('^0x.{40}$')
    if btc_regex.findall(wallet_id):
        return "BTC"
    elif eth_regex.findall(wallet_id):
        return "ETH"
    else:
        raise ValueError('Wallet not supported or improper format')


def alert(message):
    """
    Send an alert for given message.

    :param message: formatted message
    :type message: str
    :return:
    :rtype: None
    """
    print(message)
    # client = boto3.client('sns')
    # response = client.publish(
    #     TargetArn=target_arn,
    #     Message=json.dumps({'default': json.dumps(message)}),
    #     MessageStructure='json'
    # )


@click.command()
def main():
    """Entrypoint for program."""
    for wallet in wallets:
        wallet_id = wallet.get('wallet')
        wallet_format = determine_wallet_format(wallet_id)
        if wallet_format == "BTC":
            messages = check_BTC_wallet(wallet_id)
        elif wallet_format == "ETH":
            messages = check_ETH_wallet(wallet_id.lower())
        else:
            raise TypeError
        for message in messages:
            alert(message)
