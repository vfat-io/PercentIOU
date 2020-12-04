import json
import click
from brownie import MerkleDistributor, PercentIOU, Wei, accounts, interface, rpc


PERCENTIOU = "0x4De840147DB6d0655917f43dA8a2e86c26AaFB0a"
DISTRIBUTOR = "0xA742Ce2E4426290017ab165b0F7d8Ab131E4a9f5"


def get_user():
    if rpc.is_active():
        return accounts.at("0x1A6224b5ADe2C6d52d75F5d8b82197bbc61007ee", force=True)
    else:
        print("Available accounts:", accounts.load())
        return accounts.load(input("account: "))


def main():
    tree = json.load(open("snapshot/02-merkle.json"))
    user = get_user()
    dist = MerkleDistributor.at(DISTRIBUTOR, owner=user)
    piou = PercentIOU.at(PERCENTIOU, owner=user)
    if user not in tree["claims"]:
        return click.secho(f"{user} is not included in the distribution", fg="red")
    claim = tree["claims"][user]
    if dist.isClaimed(claim["index"]):
        return click.secho(f"{user} has already claimed", fg="yellow")

    amount = Wei(int(claim["amount"], 16)).to("ether")
    _amount = click.style(f"{amount:,.2f} PIOU", fg="green", bold=True)
    print(f"Claimable amount: {_amount}")
    dist.claim(claim["index"], user, claim["amount"], claim["proof"])


def burn():
    user = get_user()
    piou = PercentIOU.at(PERCENTIOU, owner=user)
    balance = piou.balanceOf(user).to("ether")
    rate = piou.rate().to("ether")
    _piou = click.style(f"{balance:,.2f} PIOU", fg="green", bold=True)
    _dai = click.style(f"{balance * rate:,.2f} DAI", fg="green", bold=True)
    _rate = click.style(f"{rate:,.5%}", fg="green", bold=True)
    _burn = click.style("burn", fg="red", bold=True)
    print(f"You have {_piou}, which can be burned for {_dai} at a rate of {_rate}")
    if click.confirm(f"Do you want to {_burn} PIOU for DAI?"):
        piou.burn()
