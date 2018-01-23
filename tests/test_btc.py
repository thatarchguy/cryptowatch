import unittest
import mock

from cryptowatch.btc import (BTC_price, BTC_to_USD,
                             check_BTC_wallet, format_BTC_message)


recv_tx = {'ver': 1, 'inputs': [{
    'sequence': 4294967295, 'witness': '', 'prev_out': {
        'spent': True, 'tx_index': 163978849, 'type': 0, 'addr': '12ZjuKhQe4ZHV3S1dttncPCCqCbJp1JMTX', 'value': 31933, 'n': 0, 'script': '76a91411293fdb354b828b0ab82fc2996df65c297b06cc88ac'
    }, 'script': '483045022100f8a81213c21397a2d2004fc81f5c6b0bc8ebe4f15f2a2ab33b74172a5663db4c022066a6fa1a08a304c619c993d5fd23ff4891f118dbd4f9e96eb0a6345166db0d640121020bca71c059f5993e1fb3ab0f8a7a8c7ab134f5bda3a74469df897ad26de6de25'}],
    'weight': 768, 'block_height': 466612, 'relayed_by': '127.0.0.1', 'out': [{
        'spent': True, 'tx_index': 251006638, 'type': 0, 'addr': '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw', 'value': 4813, 'n': 0, 'script': '76a91414a477964ed719135d1598da348a858b18b44fd588ac'}],
    'lock_time': 0, 'result': 810, 'size': 192, 'time': 1494870097, 'tx_index': 251006638, 'vin_sz': 1, 'hash': 'fd39c811a762e5ce5abd286e6c0b67eeaf66773533488fcecd871decb112e874', 'vout_sz': 1}


sent_tx = {'ver':1,'inputs':[{
    'sequence':4294967294,'witness':'','prev_out':{'spent':True,'tx_index':250001658,'type':0,'addr':'12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw','value':17124673,'n':8,'script':'76a91414a477964ed719135d1598da348a858b18b44fd588ac'},'script':'483045022100f466e70d53728e4cd222367f9236fbed484590bec57bae4a46898379bc6c34b8022053d8a12c030c7ae941ec46af7b02b32e6ea1493bf5fe83c017c38795a8a9e79b0121026eace100993a8d73f3ce1761fcfd359c015b04a9b9ebbcf9a33e9a9ca81e9c2f'}],'weight':21552,'block_height':478795,'relayed_by':'51.175.33.95','out':[{'spent':True,'tx_index':272239431,'type':0,'addr':'1JC41YHmjKEcW1rLH6pmMWEFHkoNwSmhnC','value':1227173,'n':0,'script':'76a914bc9139d7560c33087ecaf5863159f50251347dd488ac'},{'spent':True,'tx_index':272239431,'type':0,'addr':'1FQQ86tMuvhQ4Ruyggbb8j7iaNfUZ69gpY','value':871529348,'n':1,'script':'76a9149dfea13643f2d099c6148d002b4a002cb853395688ac'}],'lock_time':0,'size':5388,'double_spend':False,'time':1501729604,'tx_index':272239431,'vin_sz':36,'hash':'409803bb5e124fd028c0482027c7722e84ce55b78204b279d3a44aba5e7c1698','vout_sz':2}


class test_BTCFunctions(unittest.TestCase):

    @mock.patch('gdax.PublicClient.get_product_ticker', return_value={'price': '10000.123111'})
    def test_BTC_price(self, mocked_price):
        price = BTC_price()
        self.assertTrue(price)
        self.assertEqual(price, 10000.12)
        self.assertIsInstance(price, float)

    @mock.patch('gdax.PublicClient.get_product_ticker', return_value={'price': '10000.123111'})
    def test_BTC_to_USD(self, mocked_price):
        satoshi = 90981111
        price = BTC_to_USD(satoshi)
        self.assertTrue(price)
        self.assertEqual(price, 9098.22)
        self.assertIsInstance(price, float)
        pass

    def test_check_BTC_wallet(self):
        wallet_id = '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw'
        messages = check_BTC_wallet(wallet_id)
        self.assertTrue(messages)

    def test_format_BTC_message(self):
        wallet_id = '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw'
        message = format_BTC_message(wallet_id, recv_tx)
        self.assertIn('Received', message)

        message = format_BTC_message(wallet_id, sent_tx)
        self.assertIn('Sent', message)
