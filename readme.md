# PercentIOU

A fork of [banteg/cornichon](https://github.com/banteg/cornichonr) modified for Percent.

## Mainnet deployment

MerkleDistributor deployed at: [0xA742Ce2E4426290017ab165b0F7d8Ab131E4a9f5](https://etherscan.io/address/0xA742Ce2E4426290017ab165b0F7d8Ab131E4a9f5#code)

PercentIOU deployed at: [0x4De840147DB6d0655917f43dA8a2e86c26AaFB0a](https://etherscan.io/address/0x4De840147DB6d0655917f43dA8a2e86c26AaFB0a#code)

## Deploy

To deploy the distributor on the mainnet:

```
brownie run snapshot deploy --network mainnet
```

## Claim

To claim the distribution:
```
brownie accounts import alias keystore.json
brownie run claim --network mainnet
```

To burn PIOU for DAI:
```
brownie run claim burn --network mainnet
```

## Tests

All testing is performed in a forked mainnet environment.

To run end to end claim and burn test:

```
brownie run distribution
```

To run the unit tests:

```
brownie test
```

## Validation

To generate the snapshot data:

```
pip install -r requirements.txt

brownie networks add Ethereum archive host=$YOUR_ARCHIVE_NODE chainid=1

rm -rf snapshot
brownie run snapshot --network archive
```
