from web3 import Web3
import json

infura_url = 'your_infura_url'
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    print("Connected to Ethereum node")

    # Set contract address and abi
    contract_address = '0x44fbeBd2F576670a6C33f6Fc0B00aA8c5753b322'
    with open('contract_abi.json', 'r') as abi_file:
        contract_abi = json.load(abi_file)
        
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Set starting block number
    start_block = 12873762
    end_block = start_block + 1000  # Monitor 1000 blocks further

    # Get block information
    block = web3.eth.get_block(start_block)
    if block:
        block_number = block.number
        timestamp = block.timestamp
        print(f"Block number: {block_number}")
        print(f"Timestamp: {timestamp}")

        # Check the supply rate and borrowing rate of the block
        def get_rates(block_number):
            supply_rate = contract.functions.supplyRatePerBlock().call(block_identifier=block_number)
            borrow_rate = contract.functions.borrowRatePerBlock().call(block_identifier=block_number)
            return supply_rate, borrow_rate

        # Handle Events
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

        # Combine functions that monitor rates and events
        def monitor(start_block, end_block, step=100):
            for block in range(start_block, end_block, step):
                # Monitor interest rates
                supply_rate, borrow_rate = get_rates(block)
                print(f"#{block} supply rate: {supply_rate}")
                print(f"#{block} borrow rate: {borrow_rate}")

                # Monitor events
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

        # Start monitoring
        monitor(start_block, end_block)
    else:
        print("Failed to retrieve specified block")
else:
    print("Failed to connect to Ethereum node")
