import time
import sys
from web3 import Web3

# ==========================================================
# 🎯 ENTER ELYSIUM SNIPER v3.0 (HYPERLIQUID / ELYSIUM L2)
# ==========================================================
NFT_CONTRACT = "0x168DD252b47Ff4a63DfA98B2F0b573df4df3F3Ed"
WALLET_ADDRESS = "0xf2B38A09C6579330f55c126f852d67EAf0EF629b"
PRIVATE_KEY = "951517de88b7e7abad1cd1a0e1db5408ac171516caf97213b18bf0ad0c12fea8"

MINT_QUANTITY = 1
PRIORITY_GAS_MULTIPLIER = 2.2

# لیست RPCهای واقعی Elysium Mainnet (99901) و HyperEVM (999)
CANDIDATE_RPCS = [
    ("Elysium Mainnet (Elyscan)", "https://rpc.elyscan.live"),
    ("Elysium Mainnet (ElysPump)", "https://rpc-live.elysp.com"),
    ("HyperEVM Mainnet", "https://rpc.hyperliquid.xyz/evm"),
    ("Elysium Testnet", "https://testnet-rpc.elysium.kinetiq.xyz")
]

SEADROP_CANDIDATES = [
    "0x00005EA00Ac477B1030CE78506496e8C2dE24bf5",
    "0x00005EA00Ac477B1030CE78506496e8C2dE24bf6"
]
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
DEFAULT_FEE_RECIPIENT = "0x0000a26b00c1F0DF003000390027140000fAa719"

SEADROP_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "nftContract", "type": "address"},
            {"internalType": "address", "name": "feeRecipient", "type": "address"},
            {"internalType": "address", "name": "minterIfNotPayer", "type": "address"},
            {"internalType": "uint256", "name": "quantity", "type": "uint256"}
        ],
        "name": "mintPublic",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "nftContract", "type": "address"}],
        "name": "getPublicDrop",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint80", "name": "mintPrice", "type": "uint80"},
                    {"internalType": "uint48", "name": "startTime", "type": "uint48"},
                    {"internalType": "uint48", "name": "endTime", "type": "uint48"},
                    {"internalType": "uint16", "name": "maxTotalMintableByWallet", "type": "uint16"},
                    {"internalType": "uint16", "name": "feeBps", "type": "uint16"},
                    {"internalType": "bool", "name": "restrictFeeRecipients", "type": "bool"}
                ],
                "internalType": "struct PublicDrop",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "nftContract", "type": "address"}],
        "name": "getAllowedFeeRecipients",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]

NFT_ABI = [
    {"inputs": [{"internalType": "uint256", "name": "quantity", "type": "uint256"}], "name": "mint", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [], "name": "mint", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "quantity", "type": "uint256"}], "name": "publicMint", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "quantity", "type": "uint256"}], "name": "mintPublic", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "_receiver", "type": "address"}, {"internalType": "uint256", "name": "_quantity", "type": "uint256"}, {"internalType": "address", "name": "_currency", "type": "address"}, {"internalType": "uint256", "name": "_pricePerToken", "type": "uint256"}, {"components": [{"internalType": "bytes32[]", "name": "proof", "type": "bytes32[]"}, {"internalType": "uint256", "name": "quantityLimitPerWallet", "type": "uint256"}, {"internalType": "uint256", "name": "pricePerToken", "type": "uint256"}, {"internalType": "address", "name": "currency", "type": "address"}], "internalType": "struct IDrop.AllowlistProof", "name": "_allowlistProof", "type": "tuple"}, {"internalType": "bytes", "name": "_data", "type": "bytes"}], "name": "claim", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}
]

def discover_correct_rpc(nft_addr):
    print("=== 🔍 SCANNING FOR REAL ENTER ELYSIUM CHAIN & CONTRACT ===")
    fallback_w3 = None
    fallback_name = ""
    for name, url in CANDIDATE_RPCS:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 8}))
            if w3.is_connected():
                cid = w3.eth.chain_id
                code = w3.eth.get_code(nft_addr)
                print(f"[*] Checked {name} (ChainID: {cid}) -> Contract Bytecode: {len(code)} bytes")
                if len(code) > 2:
                    print(f"✅ [LOCKED ON] Found real contract on {name} ({url})!")
                    return w3, name, url
                if fallback_w3 is None:
                    fallback_w3, fallback_name = w3, name
        except Exception as e:
            print(f"[-] {name} unreachable: {str(e)[:40]}")
    return fallback_w3, fallback_name, CANDIDATE_RPCS[0][1]

def send_and_confirm(w3, tx_func, wallet, pk, value_wei, nonce):
    gas_est = tx_func.estimate_gas({"from": wallet, "value": value_wei})
    # یک مینت واقعی ERC721 همیشه بیش از 38,000 گس مصرف می‌کند
    if gas_est < 38000:
        raise ValueError(f"Ignored low-gas call ({gas_est} gas)")

    print(f"\n🔥 [PUBLIC MINT UNLOCKED!] Gas Est: {gas_est} | Firing Transaction Now...")
    base_gas = w3.eth.gas_price
    boosted_gas = max(int(base_gas * PRIORITY_GAS_MULTIPLIER), w3.to_wei(0.1, "gwei"))

    tx = tx_func.build_transaction({
        "from": wallet,
        "value": value_wei,
        "gas": int(gas_est * 1.35),
        "gasPrice": boosted_gas,
        "nonce": nonce,
        "chainId": w3.eth.chain_id
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=pk)
    raw_tx = getattr(signed, "raw_transaction", None) or getattr(signed, "rawTransaction", None)
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    print(f"🚀 [TX SENT] Hash: {w3.to_hex(tx_hash)}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    if receipt.status == 1 and len(receipt.logs) > 0:
        print(f"🎉 [MINT SUCCESS!] Enter Elysium NFT Minted in Block {receipt.blockNumber}!")
        return True
    else:
        print(f"⚠️ [REVERTED] Status={receipt.status}. Retrying immediately...")
        return False

def run_sniper():
    nft_addr = Web3.to_checksum_address(NFT_CONTRACT)
    w3, net_name, rpc_url = discover_correct_rpc(nft_addr)

    if not w3:
        print("❌ [ERROR] Could not connect to any Elysium / HyperEVM RPC!")
        input("Press Enter to exit...")
        sys.exit(1)

    wallet = Web3.to_checksum_address(WALLET_ADDRESS)
    pk_clean = PRIVATE_KEY.strip()
    acct = w3.eth.account.from_key(pk_clean)
    wallet = acct.address

    bal_wei = w3.eth.get_balance(wallet)
    bal_hype = float(w3.from_wei(bal_wei, "ether"))
    nft_code = w3.eth.get_code(nft_addr)

    print("\n=== 🎯 ENTER ELYSIUM SNIPER v3.0 ARMED ===")
    print(f"[*] Active Network : {net_name} (Chain ID: {w3.eth.chain_id})")
    print(f"[*] Wallet Address : {wallet}")
    print(f"[*] HYPE Balance   : {bal_hype:.6f} HYPE")
    print(f"[*] Target NFT     : {nft_addr} ({len(nft_code)} bytes)")

    if bal_hype < 0.0001:
        print("⚠️ [WARNING] Your HYPE gas balance on this network is 0.000000!")
        print("   Make sure to bridge a tiny amount of HYPE for gas before Public Mint opens tomorrow!")

    active_seadrop = None
    fee_recipient = Web3.to_checksum_address(DEFAULT_FEE_RECIPIENT)
    mint_price = 0

    for sd_cand in SEADROP_CANDIDATES:
        sd_addr = Web3.to_checksum_address(sd_cand)
        if len(w3.eth.get_code(sd_addr)) > 2:
            active_seadrop = w3.eth.contract(address=sd_addr, abi=SEADROP_ABI)
            print(f"[*] SeaDrop Router : {sd_addr} (ACTIVE)")
            try:
                recs = active_seadrop.functions.getAllowedFeeRecipients(nft_addr).call()
                if recs:
                    fee_recipient = recs[0]
                drop = active_seadrop.functions.getPublicDrop(nft_addr).call()
                mint_price = drop[0]
                print(f"[*] Public Stage   : Price={mint_price} wei | StartTS={drop[1]} | MaxPerWallet={drop[3]}")
            except Exception:
                pass
            break

    nft_contract = w3.eth.contract(address=nft_addr, abi=NFT_ABI)
    try:
        supply = nft_contract.functions.totalSupply().call()
        print(f"[*] Minted Supply  : {supply}")
    except Exception:
        pass

    print("\n⏳ [STANDBY RADAR] Monitoring blockchain... Will fire automatically the millisecond Public opens!\n")
    attempt = 0

    while True:
        attempt += 1
        last_err = "Public Stage Locked"

        try:
            if len(w3.eth.get_code(nft_addr)) <= 2:
                print(f"[WAIT #{attempt}] Contract not deployed on {net_name} yet...", end="\r", flush=True)
                time.sleep(2)
                continue

            nonce = w3.eth.get_transaction_count(wallet)

            if active_seadrop:
                try:
                    fn = active_seadrop.functions.mintPublic(nft_addr, fee_recipient, ZERO_ADDRESS, MINT_QUANTITY)
                    if send_and_confirm(w3, fn, wallet, pk_clean, mint_price * MINT_QUANTITY, nonce):
                        break
                except Exception as e:
                    last_err = f"SeaDrop: {str(e)[:45]}"

            candidate_calls = [
                ("mint(1)", lambda: nft_contract.functions.mint(MINT_QUANTITY)),
                ("publicMint(1)", lambda: nft_contract.functions.publicMint(MINT_QUANTITY)),
                ("mintPublic", lambda: nft_contract.functions.mintPublic(wallet, MINT_QUANTITY)),
                ("claim", lambda: nft_contract.functions.claim(
                    wallet, MINT_QUANTITY, "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", 0,
                    ([], 0, 0, ZERO_ADDRESS), b""
                )),
                ("mint()", lambda: nft_contract.functions.mint())
            ]

            minted = False
            for label, builder in candidate_calls:
                try:
                    fn = builder()
                    if send_and_confirm(w3, fn, wallet, pk_clean, 0, nonce):
                        minted = True
                        break
                except Exception as e:
                    if "SeaDrop" not in last_err:
                        last_err = f"{label}: {str(e)[:45]}"

            if minted:
                break

        except Exception as conn_err:
            last_err = f"RPC Reconnecting ({str(conn_err)[:30]})"

        if attempt % 4 == 0:
            clean_err = last_err.replace("\n", " ")
            print(f"📡 [RADAR #{attempt}] Status: {clean_err}                    ", end="\r", flush=True)

        time.sleep(0.25)

    input("\nPress Enter to close window...")

if __name__ == "__main__":
    run_sniper()
