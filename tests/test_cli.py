import unittest
from cryptowatch.cli import determine_wallet_format


class test_CLIFunctions(unittest.TestCase):
    def test_determine_wallet_format(self):
        self.assertEqual('ETH', determine_wallet_format('0x64623B1E4250B787568D510611989eCA71D92E1C'))
        self.assertEqual('BTC', determine_wallet_format('115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn'))
        with self.assertRaises(ValueError):
            determine_wallet_format('DEADBEEF')
