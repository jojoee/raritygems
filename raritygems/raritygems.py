import math
from Crypto.Hash import keccak
from eth_abi.packed import encode_abi_packed
import random
import time
from web3 import Web3
import requests
import datetime
from typing import Dict, List
import sys

from helper.config import ETH_GEM_ABI, FTM_GEM_ABI
from helper.notification import Notification


class Miner:
    # required
    user_address: str = ''
    chain: str = ''
    gem_kind: int
    infura_api_key: str = ""  # ETH required

    # optional
    private_key: str = ''
    line_token: str
    name: str = ''

    # internal
    w3: Web3 = None
    notification: Notification = None

    # internal (chain)
    chain_id: int = 0
    gem_address: str = ''  # e.g. "0x1234"
    gem_abi: str = ""
    provider_url: str = ""

    # internal (updated)
    user_nonce: int = 0
    gem_entropy: int = 0
    gem_difficulty: int = 0
    gem_target: int = 0
    avg_iteration_per_sec: float = 0

    # path: str = ''  # log path
    # file_logger = None
    # console_logger = None

    def __init__(
            self,
            user_address: str,
            private_key: str,
            chain: str,  # 'eth' or 'ftm',
            gem_kind: int,
            line_token: str = None,
            infura_api_key: str = None
    ):
        if chain == 'eth':
            self.chain_id = 1
            self.gem_address = "0xC67DED0eC78b849e17771b2E8a7e303B4dAd6dD4"
            self.gem_abi = ETH_GEM_ABI
            self.infura_api_key = infura_api_key
            self.provider_url = f'https://mainnet.infura.io/v3/{self.infura_api_key}'

        elif chain == 'ftm':
            self.chain_id = 250
            self.gem_address = "0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611"
            self.gem_abi = FTM_GEM_ABI
            self.provider_url = 'https://rpc.ftm.tools'
        else:
            # TODO: print something
            sys.exit()

        self.user_address = user_address
        self.private_key = private_key
        self.w3: Web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.chain = chain
        self.gem_contract = self.w3.eth.contract(
            address=self.gem_address,
            abi=self.gem_abi
        )
        self.gem_kind = gem_kind
        self.line_token = line_token

        # internal
        if line_token is not None:
            self.notification = Notification(line_token=self.line_token)

    def update_data(self):

        # get
        name, color, entropy, difficulty, \
        gems_per_mine, multiplier, crafter, \
        manager, pending_manager = self.gem_contract.functions.gems(self.gem_kind).call()
        nonce = self.gem_contract.functions.nonce(self.user_address).call()

        # assign
        self.gem_difficulty = difficulty
        self.user_nonce = nonce
        self.gem_target = 2 ** 256 / self.gem_difficulty
        self.gem_entropy = int.from_bytes(entropy, byteorder='big')

    def get_debug(self):
        msg = """gem_kind: %s\ngem_difficulty: %s\ngem_target: %s\ngem_entropy: %s\nuser_address: %s\nuser_nonce: %s
        """ % (
            self.gem_kind,
            self.gem_difficulty,
            self.gem_target,
            self.gem_entropy,
            self.user_address,
            self.user_nonce,
        )
        return msg

    def sign_transaction(self, salt):
        # TODO: optimize gas price
        transaction = self.gem_contract.functions.mine(self.gem_kind, salt).buildTransaction({
            "chainId": self.chain_id,
            "from": self.user_address,
            'gasPrice': self.w3.eth.gasPrice,
            "gas": 100000,  # TODO: config gas limit
            'nonce': self.user_nonce,
        })
        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        ticket = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        res = self.w3.eth.wait_for_transaction_receipt(ticket)
        print('transaction', transaction)
        print('res', res)

    def mine(self):
        # init
        self.update_data()
        msg = self.get_debug()
        print(msg)

        i: int = 0
        st: float = time.time()
        self.notification.line("🕒 Starting gem mining..." + msg)

        salt = 0
        while True:
            i += 1

            # check
            salt: int = random.randint(1, 2 ** 256)
            packed: bytes = encode_abi_packed(
                ['uint256', 'uint256', 'address', 'address', 'uint', 'uint', 'uint'],
                (self.chain_id, self.gem_entropy, self.gem_address, self.user_address, self.gem_kind, self.user_nonce,
                 salt,)
            )
            k = keccak.new(digest_bits=256)
            k.update(packed)
            hx: str = k.hexdigest()
            ix: int = int(hx, base=16)

            # validate
            if ix < self.gem_target:
                print(i)
                msg = self.get_debug()
                print(msg)

                msg2 = "\nsalt: %d" % salt
                self.notification.line("🎉 Gem found" + msg + msg2)

                """
                TODO recheck
                user_nonce and gem_difficulty before sign transaction for parallel processing
                """
                self.sign_transaction(salt)
                self.update_data()

            # debug
            # TODO: make ti config
            if i % 5000 == 0:
                avg_iteration_per_sec = math.floor(i / (time.time() - st))
                n_hrs = self.gem_difficulty / (
                        avg_iteration_per_sec * 60 * 60) if avg_iteration_per_sec > 0 else 0
                print("iter %d, %.2f avg iter per sec, it will take %.2f hrs to crack a salt" % (
                    i,
                    avg_iteration_per_sec,
                    n_hrs
                ))

            # TODO: make it config
            if i % 1200000 == 0:
                self.update_data()
                msg = self.get_debug()
                print(msg)
