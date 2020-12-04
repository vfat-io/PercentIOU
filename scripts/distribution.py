import json
from brownie import PercentIOU, MerkleDistributor, interface, accounts


def main():
    tree = json.load(open("snapshot/02-merkle.json"))
    whale = accounts.at("0x70178102aa04c5f0e54315aa958601ec9b7a4e08", force=True)
    dai = interface.ERC20("0x6B175474E89094C44Da98b954EedeAC495271d0F", owner=whale)
    piou = PercentIOU.at('0x4De840147DB6d0655917f43dA8a2e86c26AaFB0a', owner=whale)
    distributor = MerkleDistributor.at('0xA742Ce2E4426290017ab165b0F7d8Ab131E4a9f5', owner=whale)
    # a hacker sends everything back
    dai.transfer(piou, tree["tokenTotal"])

    for user, claim in tree["claims"].items():
        distributor.claim(claim["index"], user, claim["amount"], claim["proof"])
        assert piou.balanceOf(user) == claim["amount"]
        print("remaining in distributor:", piou.balanceOf(distributor).to("ether"))
    assert piou.balanceOf(distributor) == 0

    for user in tree["claims"]:
        user = accounts.at(user, force=True)
        amount = piou.balanceOf(user)
        before = dai.balanceOf(user)
        assert piou.rate() == "1 ether"
        piou.burn(amount, {"from": user})
        assert piou.balanceOf(user) == 0
        assert dai.balanceOf(user) == before + amount
        print("rate:", piou.rate().to("ether"))
        print("remaining supply:", piou.totalSupply().to("ether"))
        print("remaining dai:", dai.balanceOf(piou).to("ether"))

    assert dai.balanceOf(piou) == 0
    assert piou.totalSupply() == 0
