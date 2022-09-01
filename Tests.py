import unittest
import app

address = app.address
pq_deployer = app.pq_deployer


class MyTestCase(unittest.TestCase):
    # simple test for filtering
    def test_filtering(self):
        transactions_with_sell = [{"timeStamp": 126, "to": address, "from": "0x420"},
                                  {"timeStamp": 125, "to": address, "from": "0x420"},
                                  {"timeStamp": 122, "to": address, "from": "0x420"},
                                  {"timeStamp": 123, "to": "0x123", "from": "0x420"},
                                  {"timeStamp": 124, "to": address, "from": "0x420"}]
        transactions_without_sell = [{"timeStamp": 126, "to": address, "from": "0x420"},
                                     {"timeStamp": 125, "to": address, "from": "0x420"},
                                     {"timeStamp": 122, "to": address, "from": "0x420"},
                                     {"timeStamp": 124, "to": address, "from": "0x420"}]
        transactions_with_sell_last = [{"timeStamp": 126, "to": address, "from": "0x420"},
                                       {"timeStamp": 125, "to": address, "from": "0x420"},
                                       {"timeStamp": 123, "to": "0x123", "from": "0x420"},
                                       {"timeStamp": 124, "to": address, "from": "0x420"}]
        transactions_with_sell_first = [{"timeStamp": 122, "to": address, "from": "0x420"},
                                        {"timeStamp": 123, "to": "0x123", "from": "0x420"}]
        transactions_with_deployer = [{"timeStamp": 126, "to": address, "from": "0x420"},
                                      {"timeStamp": 125, "to": address, "from": pq_deployer},
                                      {"timeStamp": 122, "to": address, "from": "0x420"},
                                      {"timeStamp": 123, "to": "0x123", "from": "0x420"},
                                      {"timeStamp": 124, "to": address, "from": "0x420"}]

        result = app.filter_after_sale(transactions_with_sell)
        assert len(result) == 3

        result = app.filter_after_sale(transactions_without_sell)
        assert len(result) == 4

        result = app.filter_after_sale(transactions_with_sell_last)
        assert len(result) == 3

        result = app.filter_after_sale(transactions_with_sell_first)
        assert len(result) == 0

        result = app.filter_after_sale(transactions_with_deployer)
        assert len(result) == 2


if __name__ == '__main__':
    unittest.main()
