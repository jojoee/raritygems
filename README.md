# raritygems

[![CI and CD](https://github.com/jojoee/raritygems/actions/workflows/continuous-integration.yml/badge.svg?branch=master)](https://github.com/jojoee/raritygems/actions/workflows/continuous-integration.yml)
[![PyPI version fury.io](https://badge.fury.io/py/raritygems.svg)](https://pypi.python.org/pypi/raritygems/)
[![codecov](https://codecov.io/gh/jojoee/raritygems/branch/master/graph/badge.svg)](https://codecov.io/gh/jojoee/raritygems)

[Provably Rare Gem Raritygems](https://gems.alphafinance.io/#/rarity) API, currently focused on mining.

## Usage on Google Colab

1. Reinstall jsonschema, cause of the conflict with the Python library `web3`

```
!pip install --force-reinstall jsonschema==3.2.0
```

2. Install packages

```
!pip install web3==5.23.0
!pip install raritygems
```

3. Download [salt_finder](https://github.com/jojoee/raritygems#salt_finder) and give it permission per execute

```
!wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=10K-ZTxj14_BrY_ZxupvOkGXYl2Eo9mEq' -O raritygems_salt_finder
!chmod 755 raritygems_salt_finder
```

4. Run with Python

```python
from raritygems import raritygems

david = raritygems.Miner(
    user_address="0xxxxx",
    gem_kind=0,  # 0 = Turquoise, 1 = Pearl, ...
    salt_finder_path="/content/raritygems_salt_finder",
    private_key="",  # if "" is provided then it will only find a salt then exit
    line_token="",  # if "" is provided then it will not notify you via LINE
)
david.mine()
```

You can check more about gem kind [here](https://github.com/jojoee/raritygems/blob/master/raritygems/helper/config.py)

## How it works?

It basically finds a "salt" and sign a transaction for you. The program will do the following

1. Get the information that needed for mining: `user_nonce` and `gem_difficulty`
2. Use [salt_finder](https://github.com/jojoee/raritygems#salt_finder) to find a salt
3. Sign a transaction to claim a gem
4. Go back to step 1.

## salt_finder

At first, I start with Python and try to optimize it but I realize Go is must faster. The below is what I have tried
roughly on my local machine.

| Project | Language | Iterations per sec |
| --- | --- | --- |
| [Provably-Rare-Gem-Miner](https://github.com/yoyoismee/Provably-Rare-Gem-Miner) | Python | 2k |
| [ramen](https://github.com/dmptrluke/ramen) | JavaScript | 20k |
| [GemMiner-Go](https://github.com/TkzcM/GemMiner-Go) | Go | 30k |
| [go-gem-miner](https://github.com/sorawit/go-gem-miner) | Go | 40k |

So, I write this "salt_finder" part with Go language instead, and this is command I used to built it.

```
# to build "salt_finder"
go build -o raritygems_salt_finder main.go

# to build "salt_finder" for Google Colab
GOOS=linux GOARCH=amd64 go build -o raritygems_salt_finder_linux main.go
```

## Feature

- [ ] mining: auto update `gem_difficulty`
- [ ] lint: setup linting: flask8
- [x] ci-cd: pypi: publish to pypi
- [x] ci-cd: CI & CD with GitHub Actions
- [x] ci-cd: integrate semantic release
- [ ] test: writing automated test
- [ ] perf: performance evaluation
- [ ] info: display your current balance
- [ ] info: display your gems
- [ ] info: estimate how many times you can mine (before your have no gas left)
- [ ] gas: optimize gas price
- [ ] parallel: make it support parallel / multi-threading
- [ ] gpu: create GPU support version
- [ ] noti: refactor notification message
- [ ] noti: add more channels e.g. Facebook Messenger, email
- [x] web3: auto claim gems
- [ ] network: support Ethereum chain
- [ ] network: support Fantom network
- [ ] info: bot nickname
- [ ] salt_finder: auto load by default when it is not provided

## Project setup & CMD

TODO

```
conda create --name raritygems python=3.7.11
conda activate raritygems
pip uninstall raritygems -y && pip install .
go run main.go \
    -user-nonce=1234 \
    -user-address=0x28bc92e7b7e77d348fd262fb8e29da129308fbd3 \
    -chain-id=250 \
    -gem-difficulty=535996 \
    -gem-address=0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611 \
    -gem-entropy=0x000080440000047163a56455ac4bc6b1f1b88efadf17db76e5c52c0ca594fd9b \
    -gem-kind=0 \
    -salt=41543544848 \
    -n=800000 \
    -debug=true
```

## Ref

- [Provably Rare Gem Raritygems](https://gems.alphafinance.io/#/rarity)
