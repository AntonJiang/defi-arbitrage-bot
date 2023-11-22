from dotenv import load_dotenv
import os

from src.arb_strategy import ArbStrategy, BruteForceArbStrategy, ExecutionPlan
from src.data_processing.raw_parser import DataParser
from src.data_processing.trading_path import TradingPath
from src.db.trading_path_db import InMemoryTradingPathDB
from src.flashloan.providers import FlashloanProvider, AaveFlashloanProvider
from src.node_streaming import NodeStreaming, ContractEventDefinition, ContractEvent
from src.node_streaming.web3_pool import Web3Pool
from src.transaction_execution import (
    TransactionExecutor,
    SimulationResult,
    ExecutionResult,
)


class Bot:
    node: NodeStreaming
    w3_pool: Web3Pool
    flashloan_providers: list[FlashloanProvider]
    arb_calculator: ArbStrategy
    transaction_executor: TransactionExecutor

    def __init__(
        self,
        watching_events: list[ContractEventDefinition],
        flashloan_providers: list[FlashloanProvider],
    ):
        self.w3_pool = Web3Pool()
        self.node = NodeStreaming(
            os.environ["NODE_URL"], watching_contracts=watching_events
        )
        self.flashloan_providers = flashloan_providers

        self.data_parser = DataParser(self.w3_pool)

        self.trading_path_db = InMemoryTradingPathDB()

        self.arb_calculator = BruteForceArbStrategy(
            self.flashloan_providers, self.trading_path_db
        )

        self.transaction_executor = TransactionExecutor(self.w3_pool)

    def run(self):
        while True:
            latest_raw_events: ContractEvent = self.node.poll()

            trading_path: TradingPath = self.data_parser.parse(latest_raw_events)

            self.trading_path_db.save_path(trading_path)

            execution_plan: ExecutionPlan | None = self.arb_calculator.compute_optimal_path()

            if execution_plan is None:
                print("no possible plan so far.")
                continue

            print(f"possible execution plan: {execution_plan.final_token_amount / execution_plan.initial_token_amount} profit percentage {execution_plan} ")
            if (
                execution_plan.final_token_amount - execution_plan.initial_token_amount
                <= 0
            ):
                continue

            simulation_result: SimulationResult = (
                self.transaction_executor.simulate_transaction(execution_plan)
            )

            print(f"simulation result: {simulation_result}")

            if not simulation_result.profitable:
                continue

            execution_result: ExecutionResult = (
                self.transaction_executor.execute_transaction(execution_plan)
            )
            print(f"execution result: {execution_result}")

        self.close()

    def close(self):
        self.node.stop()


if __name__ == "__main__":
    load_dotenv()

    # TODO: hardcode a more comprehensive list of contract event definitions, more LPs, just Sync
    watching_contracts = [
        ContractEventDefinition("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Sync"),
        ContractEventDefinition(
            "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc", "Sync"
        ),  # USDC/WETH
        ContractEventDefinition(
            "0x4028DAAC072e492d34a3Afdbef0ba7e35D8b55C4", "Sync"
        ),  # stETH/WETH
        ContractEventDefinition(
            "0x25B9105cd8972F4e5df4B8eBCD06eb470794891F", "Sync"
        ),  # TONCOIN/WETH
        ContractEventDefinition(
            "0xa2107FA5B38d9bbd2C461D6EDf11B11A50F6b974", "Sync"
        ),  # LINK/WETH
        ContractEventDefinition(
            "0x819f3450dA6f110BA6Ea52195B3beaFa246062dE", "Sync"
        ),  # MATIC/WETH
        ContractEventDefinition(
            "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940", "Sync"
        ),  # WBTC/WETH
        ContractEventDefinition(
            "0x811beEd0119b4AfCE20D2583EB608C6F7AF1954f", "Sync"
        ),  # SHIB/WETH
        ContractEventDefinition(
            "0xd3d2E2692501A5c9Ca623199D38826e513033a17", "Sync"
        ),  # UNI/WETH
        ContractEventDefinition(
            "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11", "Sync"
        ),  # DAI/WETH
        ContractEventDefinition(
            "0x523a36AD73C402e456F49B04F0fe8eBA5A8C85CD", "Sync"
        ),  # LEO/WETH
        ContractEventDefinition(
            "0xb4d0d9df2738abE81b87b66c80851292492D1404", "Sync"
        ),  # TUSD/WETH
        ContractEventDefinition(
            "0x17782D58c715aa2A4458D5FB1C1d8e52a69a62Fc", "Sync"
        ),  # OKB/WETH
        ContractEventDefinition(
            "0x90704Ac59E7E54632b0CC9d22573aeCD7eB094ad", "Sync"
        ),  # CRO/WETH
        ContractEventDefinition(
            "0xC2923b8a9683556A3640ccc2961B2F52B5C4459A", "Sync"
        ),  # BUSD/WETH
        ContractEventDefinition(
            "0x454F11D58E27858926d7a4ECE8bfEA2c33E97B13", "Sync"
        ),  # LDO/WETH
        ContractEventDefinition(
            "0x0C4a68Cf6857cc76FE946d04Fe85faC5faE9625E", "Sync"
        ),  # QNT/WETH
        ContractEventDefinition(
            "0x55D5c232D921B9eAA6b37b5845E439aCD04b4DBa", "Sync"
        ),  # HEX/WETH
        ContractEventDefinition(
            "0x3C70f4FAeA49E50AdC8305F2E1Aa0EA326A54fFc", "Sync"
        ),  # INJ/WETH
        ContractEventDefinition(
            "0xc049d04D40441D77E99d77a350355d2E2EF60df1", "Sync"
        ),  # stkAAVE/WETH
        ContractEventDefinition(
            "0x2e81eC0B8B4022fAC83A21B2F2B4B8f5ED744D70", "Sync"
        ),  # GRT/WETH
        ContractEventDefinition(
            "0xC2aDdA861F89bBB333c90c492cB837741916A225", "Sync"
        ),  # MKR/WETH
        ContractEventDefinition(
            "0x0149ebe930260CcfdaAA8e3081B4C39446b6F491", "Sync"
        ),  # IMX/WETH
        ContractEventDefinition(
            "0xe4F719C11FC5AB883E32068dF99962985645E860", "Sync"
        ),  # rETH/WETH
        ContractEventDefinition(
            "0xC0a6BB3D31bb63033176edBA7c48542d6B4e406d", "Sync"
        ),  # RNDR/WETH
        ContractEventDefinition(
            "0x3dd49f67E9d5Bc4C5E6634b3F70BfD9dc1b6BD74", "Sync"
        ),  # SAND/WETH
        ContractEventDefinition(
            "0x11b1f53204d03E5529F09EB3091939e4Fd8c9CF3", "Sync"
        ),  # MANA/WETH
        ContractEventDefinition(
            "0x1ffC57cAda109985aD896a69FbCEBD565dB4290e", "Sync"
        ),  # FTM/WETH
        ContractEventDefinition(
            "0xbcF9C3e618702Ab4a0D2055687C37A2846019C56", "Sync"
        ),  # RLB/WETH
        ContractEventDefinition(
            "0xFD0A40Bc83C5faE4203DEc7e5929B446b07d1C76", "Sync"
        ),  # FRAX/WETH
        ContractEventDefinition(
            "0xff58711683Be66daD6e0e20E0043AF46FC7f5F49", "Sync"
        ),  # CHZ/WETH
        ContractEventDefinition(
            "0xb011EEaab8bF0c6DE75510128dA95498E4b7e67F", "Sync"
        ),  # APE/WETH
        ContractEventDefinition(
            "0xecBa967D84fCF0405F6b32Bc45F4d36BfDBB2E81", "Sync"
        ),  # FXS/WETH
        ContractEventDefinition(
            "0xA43fe16908251ee70EF74718545e4FE6C5cCEc9f", "Sync"
        ),  # PEPE/WETH
        ContractEventDefinition(
            "0x7f438878071228319Bd321B170EE16fC92fd6D12", "Sync"
        ),  # cETH/WETH
        ContractEventDefinition(
            "0x9C4Fe5FFD9A9fC5678cFBd93Aa2D4FD684b67C4C", "Sync"
        ),  # PAXG/WETH
        ContractEventDefinition(
            "0x598e7A017dAce2534Bc3F7496124C89425b1E165", "Sync"
        ),  # USDP/WETH
        ContractEventDefinition(
            "0xf660809B6D2D34cc43f620a9B22A40895365A5F8", "Sync"
        ),  # DYDX/WETH
        ContractEventDefinition(
            "0x2D0BA902baDAA82592f0E1C04c71d66ceA21D921", "Sync"
        ),  # BTT/WETH
        ContractEventDefinition(
            "0x6AdA49AECCF6E556Bb7a35ef0119Cc8ca795294A", "Sync"
        ),  # WOO/WETH
        ContractEventDefinition(
            "0x4042A04c54eF133aC2a3C93DB69d43C6C02a330b", "Sync"
        ),  # FET/WETH
        ContractEventDefinition(
            "0x4db44282701E28e0c2aC76188b8489298aabbC04", "Sync"
        ),  # BLUR/WETH
        ContractEventDefinition(
            "0x8Fb8BF2B444e37379e46de8BB77C551bd008f0aD", "Sync"
        ),  # ILV/WETH
        ContractEventDefinition(
            "0x2615b89AD032CcDa6D67e1D511F0E4c9e3a5dc13", "Sync"
        ),  # NEXO/WETH
        ContractEventDefinition(
            "0x26cE49c08EE71afF0C43dB8F8B9bEa950b6cdC67", "Sync"
        ),  # HT/WETH
        ContractEventDefinition(
            "0x281Cf68A2F0c04F5976867C66fd60dD3d7e0c438", "Sync"
        ),  # cbETH/WETH
        ContractEventDefinition(
            "0x26aAd2da94C59524ac0D93F6D6Cbf9071d7086f2", "Sync"
        ),  # 1INCH/WETH
        ContractEventDefinition(
            "0xCFfDdeD873554F362Ac02f8Fb1f02E5ada10516f", "Sync"
        ),  # COMP/WETH
        ContractEventDefinition(
            "0xA6F4EAE7FdaA20E632C45d4cd39E4f3961892322", "Sync"
        ),  # HBTC/WETH
        ContractEventDefinition(
            "0x5B482Ffbbdd01a629808eaf767140B5ba6c37e83", "Sync"
        ),  # NFT/WETH
        ContractEventDefinition(
            "0xB6909B960DbbE7392D405429eB2b3649752b4838", "Sync"
        ),  # BAT/WETH
        ContractEventDefinition(
            "0x0928592F80D63d474257A7b797120e301BA2d987", "Sync"
        ),  # TRB/WETH
        ContractEventDefinition(
            "0xe45b4a84E0aD24B8617a489d743c52B84B7aCeBE", "Sync"
        ),  # AGIX/WETH
        ContractEventDefinition(
            "0xca7c2771D248dCBe09EABE0CE57A62e18dA178c0", "Sync"
        ),  # FLOKI/WETH
        ContractEventDefinition(
            "0xE56c60B5f9f7B5FC70DE0eb79c6EE7d00eFa2625", "Sync"
        ),  # ENJ/WETH
        ContractEventDefinition(
            "0x3e8468f66d30Fc99F745481d4B383f89861702C6", "Sync"
        ),  # GNO/WETH
        ContractEventDefinition(
            "0x8D1cA95559ABEd542eF4402a252974221B5E1036", "Sync"
        ),  # wCELO/WETH
        ContractEventDefinition(
            "0x4D5f135691F13F7F5949AB3343ac7DC6bD7dF80B", "Sync"
        ),  # MASK/WETH
        ContractEventDefinition(
            "0x8878Df9E1A7c87dcBf6d3999D997f262C05D8C70", "Sync"
        ),  # LRC/WETH
        ContractEventDefinition(
            "0xf5ef67632cd2256d939702a126FE2c047d0a07bf", "Sync"
        ),  # HOT/WETH
        ContractEventDefinition(
            "0xDf4A9E4D3374373902Fb197FE0652a0508F5499d", "Sync"
        ),  # CVX/WETH
        ContractEventDefinition(
            "0xc03C6f5d6C5Bf2959a4E74e10fD916b5B50BF102", "Sync"
        ),  # POLY/WETH
        ContractEventDefinition(
            "0xDf4aA141031E85468137ED125749C4f6a57F8F5B", "Sync"
        ),  # MX/WETH
        ContractEventDefinition(
            "0x3BcCa6cD264709Ffc7761C9339F2f2605Fd4F24d", "Sync"
        ),  # MCO/WETH
        ContractEventDefinition(
            "0xb5F790A03b7559312D9e738df5056A4b4c8459F4", "Sync"
        ),  # GLM/WETH
        ContractEventDefinition(
            "0x3aACfbC97573ED2f57F3FeeDbacc99c52CDEEab6", "Sync"
        ),  # IOTX/WETH
        ContractEventDefinition(
            "0xB87b65Dacc6171B3ca8c4A934601d0FcB6c61049", "Sync"
        ),  # ENS/WETH
        ContractEventDefinition(
            "0x2d6f06e6f3bE6711D24f266De06F7872800f4a15", "Sync"
        ),  # cUSDT/WETH
        ContractEventDefinition(
            "0xb079D6bE3faf5771e354586DbC47d0a3D37C34fb", "Sync"
        ),  # DFI/WETH
        ContractEventDefinition(
            "0xc1f402B95196807c8f951CBe1c03C944571A1DC2", "Sync"
        ),  # WAX/WETH
        ContractEventDefinition(
            "0xaC317d14738A454Ff20B191ba3504aA97173045b", "Sync"
        ),  # SXP/WETH
        ContractEventDefinition(
            "0x2Efc769fB8Fd87AD63a38E8a0828F07C6331a734", "Sync"
        ),  # WLD/WETH
        ContractEventDefinition(
            "0x2fDbAdf3C4D5A8666Bc06645B8358ab803996E28", "Sync"
        ),  # YFI/WETH
        ContractEventDefinition(
            "0x8D9B9e25b208CAC58415d915898c2ffa3A530aa1", "Sync"
        )  # CHSB/WETH
        # WETH LP with top 100 tokens
    ]

    flashloan_providers = [AaveFlashloanProvider()]
    arb_bot = Bot(
        watching_events=watching_contracts, flashloan_providers=flashloan_providers
    )

    arb_bot.run()
