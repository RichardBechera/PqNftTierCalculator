from bscscan import BscScan
import asyncio
from datetime import datetime
from urllib.request import Request, urlopen
import re
from py_linq import Enumerable

urlForm = "https://bscscan.com/tx/"
closing = r'<span id="ContentPlaceHolder1_spanClosingPrice">\$(\d*\.\d*) / BNB</span>'
curent = r'<span data-toggle="tooltip" data-original-title="Current Price : \$\d*\.\d* / WBNB">(\d*\.\d*) .*</span>'

address = "<YOUR ADDRESS>"
contract = "0xA38898a4Ae982Cb0131104a6746f77fA0dA57aAA"  # QBIT contract address

tiers = {"Bronze": 500,
         "Silver": 1500,
         "Gold": 4000,
         "Platinum": 10000,
         "Diamond": 25000,
         "Quantum": 50000}


# Get all transactions of given address on given contract
async def get_transfers_paginated(contract_address: str, user_address: str, page: int, offset: int, sort: str):
    async with BscScan("<YOUR API KEY>") as client:
        return await client.get_bep20_token_transfer_events_by_address_and_contract_paginated(
            contract_address, user_address, page, offset, sort)


# This is stupid but API endpoint for that from BnbScan is paid and I'm poor
# Get html of BscScan transaction page
def get_html(tx_hash: str):
    url = f"{urlForm}{tx_hash}"

    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    return urlopen(req).read().decode()


# Match prices from BscScan transaction page and calculate price of transaction at the time of buying
def calculate_transaction_dolar_price(page: str):
    current_match = re.search(curent, page)
    current_value = float(current_match.groups()[0])
    closing_match = re.search(closing, page)
    closing_value = float(closing_match.groups()[0])
    return current_value * closing_value


# Add up all the costs of transactions and decide under which tier it falls
def decide_tier(transactions, print_all):
    total = 0

    for transaction in transactions:
        if print_all:
            print(datetime.fromtimestamp(int(transaction["timeStamp"])))
            print(f'{transaction["value"]} QBIT')

        page = get_html(transaction["hash"])
        value = calculate_transaction_dolar_price(page)
        total += value

        if print_all:
            print(f'Transaction cost {value}')
            print()

    print(f"Total cost: {total}")
    print(f"Your tier: {tier_from_value(total)}")


# Return tier based on price
def tier_from_value(value):
    if value >= tiers["Bronze"]:
        return "Bronze"
    elif value >= tiers["Silver"]:
        return "Silver"
    elif value >= tiers["Gold"]:
        return "Gold"
    elif value >= tiers["Platinum"]:
        return "Platinum"
    elif value >= tiers["Diamond"]:
        return "Diamond"
    elif value >= tiers["Quantum"]:
        return "Quantum"


# filter all the transactions happening before sale
def filter_after_sale(transactions):
    collection = Enumerable(transactions)
    ordering = lambda transaction: int(transaction["timeStamp"])
    condition = lambda transaction: transaction["to"] == address

    return collection.order_by_descending(ordering).take_while(condition).to_list()


async def main():
    transactions = await get_transfers_paginated(contract, address, 1, 100, "asc")
    transactions = filter_after_sale(transactions)
    decide_tier(transactions, False)

asyncio.run(main())


# simple test for filtering
def test_filtering():
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

    result = filter_after_sale(transactions_with_sell)
    assert len(result) == 3

    result = filter_after_sale(transactions_without_sell)
    assert len(result) == 4

    result = filter_after_sale(transactions_with_sell_last)
    assert len(result) == 3

    result = filter_after_sale(transactions_with_sell_first)
    assert len(result) == 0


#test_filtering()
