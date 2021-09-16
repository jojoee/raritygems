package main

import (
	"flag"
	"fmt"
	"github.com/ethereum/go-ethereum/common"
	solsha3 "github.com/miguelmota/go-solidity-sha3"
	"math/big"
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
}

func main() {
	// flag
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
	}
	flag.Parse()

	userNonce := int64(*cPtr.userNonce)
	userAddress := *cPtr.userAddress
	chainId := int64(*cPtr.chainId)
	gemDifficulty := big.NewInt(int64(*cPtr.gemDifficulty))
	gemAddress := *cPtr.gemAddress
	gemEntropy := *cPtr.gemEntropy
	gemKind := int64(*cPtr.gemKind)
	salt, _ := new(big.Int).SetString(*cPtr.saltStart, 10)
	debug := *cPtr.debug

	// const
	plus := big.NewInt(1)
	max, _ := new(big.Int).SetString("115792089237316195423570985008687907853269984665640564039457584007913129639935", 10)
	target := new(big.Int).Div(max, gemDifficulty)

	// debug
	if debug {
		fmt.Printf("userNonce: %d\n", userNonce)
		fmt.Printf("gemDifficulty: %d\n", gemDifficulty)
		fmt.Printf("gemAddress: %s\n", gemAddress)
		fmt.Printf("gemEntropy: %s\n", gemEntropy)
		fmt.Printf("gemKind: %d\n", gemKind)
		fmt.Printf("userAddress: %s\n", userAddress)
		fmt.Printf("salt: %v\n", salt)
	}

	total := 0
	for true {
		hash := solsha3.SoliditySHA3(
			// types
			[]string{"uint256", "bytes32", "address", "address", "uint256", "uint256", "uint256"},

			// values
			[]interface{}{
				chainId,
				"0x000080440000047163a56455ac4bc6b1f1b88efadf17db76e5c52c0ca594fd9b", // gem entropy
				common.HexToAddress("0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611"),    // gem address
				common.HexToAddress(userAddress),                                     // user_address
				big.NewInt(gemKind),
				big.NewInt(userNonce),
				salt,
			},
		)

		total += 1

		var luck = new(big.Int).SetBytes(hash)
		//if luck.Cmp(target) != 1 {
		//	fmt.Println(salt)
		//	break
		//}

		if total >= 10000 {
			fmt.Println(luck)
			fmt.Println(target)
			break
		}

		salt.Add(salt, plus)
	}
}
