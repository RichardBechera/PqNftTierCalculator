import unittest
import TierCalculator

address = TierCalculator.address


class MyTestCase(unittest.TestCase):
    # simple test for filtering
    def test_filtering(self):
        transactions_with_sell = [{"timeStamp": 126, "to": address},
                                  {"timeStamp": 125, "to": address},
                                  {"timeStamp": 122, "to": address},
                                  {"timeStamp": 123, "to": "0x123"},
                                  {"timeStamp": 124, "to": address}]
        transactions_without_sell = [{"timeStamp": 126, "to": address},
                                     {"timeStamp": 125, "to": address},
                                     {"timeStamp": 122, "to": address},
                                     {"timeStamp": 124, "to": address}]
        transactions_with_sell_last = [{"timeStamp": 126, "to": address},
                                       {"timeStamp": 125, "to": address},
                                       {"timeStamp": 123, "to": "0x123"},
                                       {"timeStamp": 124, "to": address}]
        transactions_with_sell_first = [{"timeStamp": 122, "to": address},
                                        {"timeStamp": 123, "to": "0x123"}]

        result = TierCalculator.filter_after_sale(transactions_with_sell)
        assert len(result) == 3

        result = TierCalculator.filter_after_sale(transactions_without_sell)
        assert len(result) == 4

        result = TierCalculator.filter_after_sale(transactions_with_sell_last)
        assert len(result) == 3

        result = TierCalculator.filter_after_sale(transactions_with_sell_first)
        assert len(result) == 0


if __name__ == '__main__':
    unittest.main()
