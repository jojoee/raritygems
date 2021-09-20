import subprocess
import random
import sys
from time import sleep
import traceback
from web3 import Web3, contract
from raritygems.helper.config import FTM_GEM_ABI
from raritygems.helper.notification import line


class Miner:
    # required
    user_address: str
    gem_kind: int
    private_key: str
    line_token: str

    # internal
    w3: Web3
    gem_contract: contract.Contract

    # internal (chain)
    chain_id: int = 250
    gem_address: str = "0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611"  # contract address
    gem_entropy: str = "0x000080440000047163a56455ac4bc6b1f1b88efadf17db76e5c52c0ca594fd9b"
    gem_abi: str = FTM_GEM_ABI
    provider_url: str = 'https://rpc.ftm.tools'

    def __init__(
            self,
            user_address: str,
            private_key: str,
            gem_kind: int,
            line_token: str,
            salt_finder_path: str,
    ):
        # user provided
        self.user_address = user_address
        self.gem_kind = gem_kind
        self.private_key = private_key
        self.line_token = line_token
        self.salt_finder_path = salt_finder_path

        # init
        self.w3: Web3 = Web3(Web3.HTTPProvider(self.provider_url))
        self.gem_contract = self.w3.eth.contract(address=self.gem_address, abi=self.gem_abi)

    def sign_transaction(self, salt):
        td = {
            "chainId": self.chain_id,
            "from": self.user_address,
            'gasPrice': self.w3.eth.gasPrice,
            "gas": 100000,  # TODO: config gas limit
            'nonce': self.w3.eth.get_transaction_count(self.user_address),
        }
        print('building transaction %s' % str(td))
        transaction = self.gem_contract.functions.mine(self.gem_kind, salt).buildTransaction(td)
        print('sign transaction')
        signed_tx = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print('transaction', transaction)
        print('txn_hash', tx_hash)
        print('tx_receipt', tx_receipt)
        print("tx_receipt['transactionHash']", tx_receipt['transactionHash'].hex())

    def mine(self, n: int = 25000 * 60 * 60 * 2):
        """
        :param n: restart every n iterations
        :return:
        """
        msg = '🕒 Start mining'
        print(msg)

        while True:
            try:
                # arrange
                salt = random.randint(1, 2 ** 256)
                gem_difficulty: int = self.gem_contract.functions.gems(self.gem_kind).call()[3]
                user_nonce: int = self.gem_contract.functions.nonce(self.user_address).call()
                d = {
                    'gem_kind': self.gem_kind,
                    'gem_difficulty': gem_difficulty,
                    'user_address': self.user_address,
                    'user_nonce': user_nonce,
                    'salt': salt,
                }
                msg = '💡start next loop %s' % str(d)
                print(msg)
                line(self.line_token, msg)

                # act
                res = subprocess.check_output([
                    self.salt_finder_path,
                    '-user-nonce', str(user_nonce),
                    '-user-address', self.user_address,
                    '-chain-id', str(self.chain_id),
                    '-gem-difficulty', str(gem_difficulty),
                    '-gem-address', self.gem_address,
                    '-gem-entropy', self.gem_entropy,
                    '-gem-kind', str(self.gem_kind),
                    '-salt', str(salt),  # starter salt
                    '-n', str(n),
                ], universal_newlines=True, stderr=subprocess.STDOUT)
                print("res", res)

                # sign
                target_salt = int(res)
                d['salt'] = target_salt
                msg = '🎉 Gem found %s' % str(d)

                if target_salt == -1:
                    # just restart or update the data
                    print('🔄 update the value')
                else:
                    line(self.line_token, msg)
                    print(msg)
                    if not self.private_key:
                        sys.exit()
                    self.sign_transaction(target_salt)

                    # TODO: get tx status before go next loop (success or fail)
                    print('you are tired for mint one sleep for 16 secs')
                    sleep(16)  # sleep 16 second before get new loop

            except Exception as e:
                line(self.line_token, '🔥🔥🔥🔥🔥🔥🔥🔥\n ERROR %s' % str(e))
                print('An exception occurred: {}'.format(e))

                print('traceback.print_exc()')
                traceback.print_exc()

                print('traceback.format_exc()')
                fes = traceback.format_exc()
                print(fes)

                print('error then go sleep for 16 secs')
                sleep(16)
