from dotenv import load_dotenv
import os

from src.arb_strategy import ArbStrategy, BruteForceArbStrategy, ExecutionPlan
from src.data_processing.raw_parser import DataParser
from src.data_processing.trading_path import TradingPath
from src.db.trading_path_db import InMemoryTradingPathDB
from src.flashloan.providers import FlashloanProvider, AaveFlashloanProvider
from src.node_streaming import NodeStreaming, ContractEventDefinition, ContractEvent
from src.transaction_execution import TransactionExecutor, SimulationResult, ExecutionResult


class Bot:
    node: NodeStreaming
    flashloan_providers: list[FlashloanProvider]
    arb_calculator: ArbStrategy
    transaction_executor: TransactionExecutor

    def __init__(self, watching_events: list[ContractEventDefinition],
                 flashloan_providers: list[FlashloanProvider]):
        self.node = NodeStreaming(os.environ["NODE_URL"], watching_contracts=watching_events)
        self.flashloan_providers = flashloan_providers

        self.data_parser = DataParser()

        self.trading_path_db = InMemoryTradingPathDB()

        self.arb_calculator = BruteForceArbStrategy(self.flashloan_providers, self.trading_path_db)

        self.transaction_executor = TransactionExecutor()

    def run(self):
        while True:
            latest_raw_events: ContractEvent = self.node.poll()

            trading_path: TradingPath = self.data_parser.parse(latest_raw_events)

            self.trading_path_db.save_path(trading_path)

            execution_plan: ExecutionPlan = self.arb_calculator.compute_optimal_path()

            print(f"possible execution plan: {execution_plan}")
            if execution_plan.final_token_amount - execution_plan.initial_token_amount <= 0:
                continue

            simulation_result: SimulationResult = self.transaction_executor.simulate_transaction(execution_plan)

            print(f"simulation result: {simulation_result}")

            if not simulation_result.profitable:
                continue

            execution_result: ExecutionResult = self.transaction_executor.execute_transaction(execution_plan)
            print(f"execution result: {execution_result}")

        self.close()

    def close(self):
        self.node.stop()


if __name__ == '__main__':
    load_dotenv()

  
    # TODO: hardcode a more comprehensive list of contract event definitions, more LPs, just Sync


    watching_contracts = [ContractEventDefinition("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Sync"),
                          ContractEventDefinition("0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc", "Sync"), #USDC/WETH
                          ContractEventDefinition("0x4028DAAC072e492d34a3Afdbef0ba7e35D8b55C4", "Sync"), #stETH/WETH
                          ContractEventDefinition("0x25B9105cd8972F4e5df4B8eBCD06eb470794891F", "Sync"), #TONCOIN/WETH 
                          ContractEventDefinition("0xa2107FA5B38d9bbd2C461D6EDf11B11A50F6b974", "Sync"), #LINK/WETH
                          ContractEventDefinition("0x819f3450dA6f110BA6Ea52195B3beaFa246062dE", "Sync"), #MATIC/WETH
                          ContractEventDefinition("0xBb2b8038a1640196FbE3e38816F3e67Cba72D940", "Sync"), #WBTC/WETH
                          ContractEventDefinition("0x811beEd0119b4AfCE20D2583EB608C6F7AF1954f", "Sync"), #SHIB/WETH
                          ContractEventDefinition("0xd3d2E2692501A5c9Ca623199D38826e513033a17", "Sync"), #UNI/WETH
                          ContractEventDefinition("0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11", "Sync"), #DAI/WETH
                          ContractEventDefinition("0x523a36AD73C402e456F49B04F0fe8eBA5A8C85CD", "Sync"), #LEO/WETH
                          ContractEventDefinition("0xb4d0d9df2738abE81b87b66c80851292492D1404", "Sync"), #TUSD/WETH
                          ContractEventDefinition("0x17782D58c715aa2A4458D5FB1C1d8e52a69a62Fc", "Sync"), #OKB/WETH
                          ContractEventDefinition("0x90704Ac59E7E54632b0CC9d22573aeCD7eB094ad", "Sync"), #CRO/WETH
                          ContractEventDefinition("0xC2923b8a9683556A3640ccc2961B2F52B5C4459A", "Sync"), #BUSD/WETH
                          ContractEventDefinition("0x454F11D58E27858926d7a4ECE8bfEA2c33E97B13", "Sync"), #LDO/WETH
                          ContractEventDefinition("0x0C4a68Cf6857cc76FE946d04Fe85faC5faE9625E", "Sync"), #QNT/WETH
                          ContractEventDefinition("0x55D5c232D921B9eAA6b37b5845E439aCD04b4DBa", "Sync"), #HEX/WETH
                          ContractEventDefinition("0x3C70f4FAeA49E50AdC8305F2E1Aa0EA326A54fFc", "Sync"), #INJ/WETH
                          ContractEventDefinition("0xc049d04D40441D77E99d77a350355d2E2EF60df1", "Sync"), #stkAAVE/WETH
                          ContractEventDefinition("0x2e81eC0B8B4022fAC83A21B2F2B4B8f5ED744D70", "Sync"), #GRT/WETH
                          ContractEventDefinition("0xC2aDdA861F89bBB333c90c492cB837741916A225", "Sync"), #MKR/WETH
                          ContractEventDefinition("0x0149ebe930260CcfdaAA8e3081B4C39446b6F491", "Sync"), #IMX/WETH
                          ContractEventDefinition("0xe4F719C11FC5AB883E32068dF99962985645E860", "Sync"), #rETH/WETH
                          ContractEventDefinition("0xC0a6BB3D31bb63033176edBA7c48542d6B4e406d", "Sync"), #RNDR/WETH
                          ContractEventDefinition("0x3dd49f67E9d5Bc4C5E6634b3F70BfD9dc1b6BD74", "Sync"), #SAND/WETH
                          ContractEventDefinition("0x11b1f53204d03E5529F09EB3091939e4Fd8c9CF3", "Sync"), #MANA/WETH
                          ContractEventDefinition("0x1ffC57cAda109985aD896a69FbCEBD565dB4290e", "Sync"), #FTM/WETH
                          ContractEventDefinition("0xbcF9C3e618702Ab4a0D2055687C37A2846019C56", "Sync"), #RLB/WETH
                          ContractEventDefinition("0xFD0A40Bc83C5faE4203DEc7e5929B446b07d1C76", "Sync"), #FRAX/WETH



                         ] 
    
    


    flashloan_providers = [AaveFlashloanProvider()]
    arb_bot = Bot(watching_events=watching_contracts,
                  flashloan_providers=flashloan_providers)

    arb_bot.run()
