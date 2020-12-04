import json
from brownie import MerkleDistributor, PercentIOU, accounts, rpc, interface, Contract


def main():
    tree = json.load(open("snapshot/02-merkle.json"))
    user = accounts[0] if rpc.is_active() else accounts.load(input("account: "))
    root = tree["merkleRoot"]
    percentIOU = PercentIOU.deploy(
        "Percent IOU", "PIOU", tree["tokenTotal"], {"from": user}
    )
    distributor = MerkleDistributor.deploy(percentIOU, root, {"from": user})
    percentIOU.transfer(distributor, percentIOU.balanceOf(user))
