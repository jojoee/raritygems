package main

import (
	"flag"
	"fmt"
	"github.com/ethereum/go-ethereum/common"
	solsha3 "github.com/miguelmota/go-solidity-sha3"
	"math/big"
	"time"
)

type ConfigPtr struct {
	userNonce     *int
	userAddress   *string
	chainId       *int
	gemDifficulty *int
	gemAddress    *string
	gemEntropy    *string
	gemKind       *int
	saltStart     *string
	debug         *bool
	n             *int
}

func main() {
	// flag
	var defaultN = 25000 * 60 * 60 * 2 // !2 hrs
	var cPtr = ConfigPtr{
		flag.Int("user-nonce", 0, "User nonce"),
		flag.String("user-address", "0xxxx", "User Fantom wallet address"),
		flag.Int("chain-id", 250, "Chain ID"),
		flag.Int("gem-difficulty", 0, "Gem difficult"),
		flag.String("gem-address", "0xxxx", "Gem contract address"),
		flag.String("gem-entropy", "0xxxx", "Gem entropy"),
		flag.Int("gem-kind", 0, "Gem kind"),
		flag.String("salt", "2300000", "Starter salt"),
		flag.Bool("debug", false, "Is debug version"),
		flag.Int("n", defaultN, "max number of iterations"), // default ~2 hrs
	}
	flag.Parse()

	userNonce := big.NewInt(int64(*cPtr.userNonce))
	userAddress := common.HexToAddress(*cPtr.userAddress)
	chainId := big.NewInt(int64(*cPtr.chainId))
	gemDifficulty := big.NewInt(int64(*cPtr.gemDifficulty))
	gemAddress := common.HexToAddress(*cPtr.gemAddress)
	gemEntropy := *cPtr.gemEntropy
	gemKind := big.NewInt(int64(*cPtr.gemKind))
	salt, _ := new(big.Int).SetString(*cPtr.saltStart, 10)
	debug := *cPtr.debug
	n := int64(*cPtr.n)

	// const
	total := int64(0)
	plus := big.NewInt(1)
	max, _ := new(big.Int).SetString("115792089237316195423570985008687907853269984665640564039457584007913129639935", 10)
	target := new(big.Int).Div(max, gemDifficulty)
	start := time.Now().UnixNano()

	// debug
	if debug {
		fmt.Printf("userNonce: %d\n", userNonce)
		fmt.Printf("userAddress: %s\n", userAddress)
		fmt.Printf("chainId: %d\n", chainId)
		fmt.Printf("gemDifficulty: %d\n", gemDifficulty)
		fmt.Printf("gemAddress: %s\n", gemAddress)
		fmt.Printf("gemEntropy: %s\n", gemEntropy)
		fmt.Printf("gemKind: %d\n", gemKind)
		fmt.Printf("salt: %v\n", salt)
		fmt.Printf("n: %d\n", n)
	}

	for true {
		// init
		total += 1

		// process
		hash := solsha3.SoliditySHA3(
			[]string{"uint256", "bytes32", "address", "address", "uint256", "uint256", "uint256"},
			[]interface{}{chainId, gemEntropy, gemAddress, userAddress, gemKind, userNonce, salt},
		)

		var luck = new(big.Int).SetBytes(hash)
		if luck.Cmp(target) != 1 {
			fmt.Print(salt)
			break
		}

		// restart
		if total >= n {
			fmt.Print(-1)
			break
		}

		// debug
		if debug {
			now := time.Now().UnixNano()
			secs := (now-start)/1e9 + 1
			fmt.Printf("\rtotal hashes %d in %d secs, hashes per second : %d", total, secs, total/secs)
		}

		// next
		salt.Add(salt, plus)
	}
}
