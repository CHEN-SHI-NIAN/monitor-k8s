from web3 import Web3
import json

infura_url = 'https://mainnet.infura.io/v3/f3fa5aac4b1549bf8b3eceb0b3086ef8'
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    print("Connected to Ethereum node")

    # 設定合約地址和 ABI
    contract_address = '0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322'
    with open('contract_abi.json', 'r') as abi_file:
        contract_abi = json.load(abi_file)
        
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # 設定起始區塊號
    start_block = 12873762
    end_block = start_block + 1000  # 假設要往後監控 1000 個區塊

    # 獲取區塊資訊
    block = web3.eth.get_block(start_block)
    if block:
        block_number = block.number
        timestamp = block.timestamp
        print(f"Block number: {block_number}")
        print(f"Timestamp: {timestamp}")

        # 查詢指定區塊的供應利率和借款利率
        def get_rates(block_number):
            supply_rate = contract.functions.supplyRatePerBlock().call(block_identifier=block_number)
            borrow_rate = contract.functions.borrowRatePerBlock().call(block_identifier=block_number)
            return supply_rate, borrow_rate

        # 處理事件
        def handle_event(event):
            tx_hash = event['transactionHash'].hex()
            block_number = event['blockNumber']
            event_type = event['event']
            decoded_args = dict(event['args'])

            if event_type == 'Mint':
                print(f"#{block_number}: {tx_hash}")
                print(f"{decoded_args['minter']} Mint {decoded_args['mintTokens']} crUSDC with {decoded_args['mintAmount']} USDC")
            elif event_type == 'Redeem':
                print(f"#{block_number}: {tx_hash}")
                print(f"{decoded_args['redeemer']} Redeem {decoded_args['redeemAmount']} USDC, burn {decoded_args['redeemTokens']} crUSDC")
            elif event_type == 'Borrow':
                print(f"#{block_number}: {tx_hash}")
                print(f"{decoded_args['borrower']} Borrow {decoded_args['borrowAmount']} USDC")
            elif event_type == 'RepayBorrow':
                print(f"#{block_number}: {tx_hash}")
                print(f"{decoded_args['payer']} RepayBorrow {decoded_args['repayAmount']} USDC for {decoded_args['borrower']}")

        # 合并監控利率和事件的函數
        def monitor(start_block, end_block, step=100):
            for block in range(start_block, end_block, step):
                # 監控利率
                supply_rate, borrow_rate = get_rates(block)
                print(f"#{block} supply rate: {supply_rate}")
                print(f"#{block} borrow rate: {borrow_rate}")

                # 監控事件
                mint_filter = contract.events.Mint.create_filter(fromBlock=block, toBlock=block + step - 1)
                redeem_filter = contract.events.Redeem.create_filter(fromBlock=block, toBlock=block + step - 1)
                borrow_filter = contract.events.Borrow.create_filter(fromBlock=block, toBlock=block + step - 1)
                repay_borrow_filter = contract.events.RepayBorrow.create_filter(fromBlock=block, toBlock=block + step - 1)

                for event in mint_filter.get_all_entries():
                    handle_event(event)
                for event in redeem_filter.get_all_entries():
                    handle_event(event)
                for event in borrow_filter.get_all_entries():
                    handle_event(event)
                for event in repay_borrow_filter.get_all_entries():
                    handle_event(event)

        # 開始監控
        monitor(start_block, end_block)
    else:
        print("Failed to retrieve specified block")
else:
    print("Failed to connect to Ethereum node")