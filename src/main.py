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


    #list of transaction hashes with WETH 
    txn_hash = ["0x7cd937a5febcdde91006dbde0ba9c96ba7b5fe0b10fc5b8e1acd06e85062c99e", "0x6ec6b6ad0ecd0693f9e9b69a4eba7b03197fa7477a7f07ac7d388df33f6b4103",
                "0xe7749763a3e4dc92248bb474ab2a1da462d67b3947c1184cbca539162782fa64", "0xbcac9dbd1364c0ef15a3b2b16a4a74c3a1cb52739d3f54c748f2f2cda0f1354b",
                "0xe1ed0de50a0f25ec693e44e2df54f3db092d087af85f9e6eb1636effc85042f4", "0x8cbf5851b912761ff3efe3489389f513db7eca960084c4fea2f4b465fb1dc7dc",
                "0x3f49638ca91f4b3146ec79449ad0a70c75754dd7b2d30d433149f26dc4adc982", "0x3f49638ca91f4b3146ec79449ad0a70c75754dd7b2d30d433149f26dc4adc982",
                "0x2678aa49fab26086f6087666abc2df70a64dce01f06b713ee191e0796308629f", "0x4c98877249b2d2e43e3c9fb664c76158ca84f1b15fd9b0e99ecff0d2e4289ac7",
                "0xbb0d31ceeced984e91944fec34ed7ffb2bf15ad0625cd4fe376a6bb968d77342", "0xbb0d31ceeced984e91944fec34ed7ffb2bf15ad0625cd4fe376a6bb968d77342",
                "0xdd6d5443bb712bf2b591b9175dd33b338284ff51e46de55f5a95e960c22afe33", "0xd9a6d9fb10d33c443786ea4c04cf49a86e64670be876d0327722961a04479b9a",
                "0x8fd05b6a5fd1017dab0ca2b7cea7704fe5e9d0c5d69f08d2eb48652ad9f6e98d", "0x868434d555fe8130da8542319df860758e5731e4795beb00b32b3475fe672694",
                "0x868434d555fe8130da8542319df860758e5731e4795beb00b32b3475fe672694", "0x42fc307661515dd737c2b5ebc048a4909b4a3c826fc96599742dbb5a13f3490a",
                "0x106ff8fb44539b4e975b2bd800a49d295f646f8d2b750cea5f123959ba0ba27d", "0x313ab090c5ca55fcfb2b02a0d1a0755515649895a56e0ba1e274c79a012f18d4",
                "0x958d7869558ef36acc8eed9f51f5e2ad67bcb22941315a6fe666bee64ad10137", "0x05322668ab10a8584a5aa512fa8e81117e069675ed7c6782de4f901def5d94ea",
                "0xe822fc3e86ef88541195cf487419d3181338963b54e21ddd879fd6f526819938", "0x905e943cf0321ab8f237a2ab854e1a26683531188abc12bad64762b5caf4b027",
                "0xdbf6147dfac838c38a925ece6e4a6edd03785f869a39045df74ba86cf09bee15", "0x1bd9acaf1d46ae6afcc31d4cf90902000948effccf0fceb185e1f2846ae54478",
                "0x6ee419e3354afa0ad9aa076bf0736dac2401fbf39508b6a455b2b201302a1ad8", "0x6ee419e3354afa0ad9aa076bf0736dac2401fbf39508b6a455b2b201302a1ad8",
                "0x45c1195892b56989eee55b9d8e372c795b8966ba8c1d601ff77378f2b2948664", "0x5de028be56c24eed938765627537a57e4ecd5d61b71cc50b275787278e9a558a",
                "0x39b10a5e65e223d8231df25bcacb28bab7024c7f9c6d59c3637105050d3db084", "0xdc6b8e0a9efcb10a1294ced2f1871ba864712b54cdb7491b5e13cc7af049d4bd",
                "0xee9d098ead4e4b5e26227b21e36c840b77b9aca2dffbe56ce06404c6d0164135", "0x67c15334f830401cb9234fd6438a4f5a90da815fa7ec383cefb2e4c85f94a40a",
                "0x6b8cb747184e8a9a0c0388ee3d1a2bcaba46821f832c040a13d8045ae6772c79", "0x32f32995beb1d41a36dacf84fe2b7655daef800bd583c747fb2c3aebb3189c32",
                "0x32f32995beb1d41a36dacf84fe2b7655daef800bd583c747fb2c3aebb3189c32", "0x9c2f54f85203b80c49089a66a87d8e2329a390358fda2e8d618d3afad6957344",
                "0x14d90fbb90cd37330ee5f2533e5e16500e028ae13a0fe4a37f1b614a2ca8ffee", "0x97132e0287af6711fa62c65075d2046f52a042ca7ba6a301a7c2a3910287934f",
                "0x0c7d9f3512e6b8ed76dd5c0555483904898b92f9918d7b903619c463eccaf1a2", "0x473351719bc7bf02147ad8c525c106925983a70e967f53491c0bbc52459e8796",
                "0x473351719bc7bf02147ad8c525c106925983a70e967f53491c0bbc52459e8796", "0x72159b53fe6cf9110fc0adb97f603bb806b256ecb4da17b11566e066624d51a8",
                "0x4919d3e7e94506d3c22e1f013ae3206260b7ab51f948c0dcdea1dbd5baa20546", "0x10c458e6fcca13e9f6625b451243f2d50ba3dc30f7ddb5b7f94062dc4c4327d9",
                "0x5a2eadc464db76a9c2bf78d1762fc2497bb2cb1ac261d442ab8dca2140fb1dd3", "0x9eee1fe9be60060ea7cb52c419828ff03f05eda886ad2dcbb8312360382b8477",
                "0xae4dd6b34bda4170762f31726f840f85d195248b3b59f6371ed57eee646132e5", "0xae4dd6b34bda4170762f31726f840f85d195248b3b59f6371ed57eee646132e5",
                "0x7b7fdc4e20259b840d0085df0f78b517585f19d4c84da133859cdc18ea4e4f59", "0xaaf12fbac692b368d23d869c8a209f87c7a93250804df1d91472143d16683c6e",
                "0xb66766a292a99b19b07a70b37b3c176d4b9f98494c60bdfc29a6cf79bbf7a137", "0x1502f01f12412c6b6379e693848c1321117aa3e9a4b43d92c200e6d2cc61a4a1",
                "0x48e4e8fdff01e8adc2fb76893de57c62462a408ce8118590266fd883abf03363", "0x8117b54c10bbdb93821c6466b8902511d3449a0843c2981efb0b842e94c5f0c7",
                "0xf904360eee93375f5112a63e6a47d6247488f031c4c5bae6684284227d2d5171", "0x579e4cd5a13e5ed6c9ee9178bd9a1e18b6c31d67f5e70549bba0723d14126ea3",
                "0xb8697d735f4873f18eb841ab48cdf1408350b30da8a14ab3eabc6f3ec14c3755", "0xeb74b08f7e14af0265870a76ef4500b32e96fe238fd056186de80ee3d95ee9ee",
                "0x6ee6074ef2855b08329310dbd33677372fc43e65de144390c05c77c1d411acb4", "0x94774576d7edf447b57c28c9c839109e7b7447457cba947b6904ce42ab2a036d",
                "0xf0f9ca3686ae5bc8cca8f96591a67a7db1aa8f57d7bd6e8467b181b25e6755ea", "0xca691c9fb0044fc7f6341554bb9d78dded25b2ee9730e600c7d1afe8fe1db726",
                "0xcaed642c238811782ee86155ecf585a27d646a052a55c7a4229b6f914ca0b795", "0xcaed642c238811782ee86155ecf585a27d646a052a55c7a4229b6f914ca0b795",
                "0xd464d705d1956d12684a8d352632de4a27d251a315c5e481018f4aa9f8c74448", "0x336259fe2b311547cf60b2adeefad7d40de1a6a20c5e80949372a2650f6a9e4f",
                "0x111ffdc5ddf8c4d6e5e45f07af33d222a40d1db48a9e7b3ec217834221f196e0", "0xbfd18dd828abd9296bda799ccd4ae74ad182f72990ff2417d04ad407c55f0c75",
                "0x005a675854eb0e8e5c51e01dc9c5217af7e3c04974d220ba95f777982c30c823", "0x3773aa3f3174730d0427e3d3b8fdedcd8b19a73e3565bbdb3c4541c8bc24ac78",
                "0xb3869fb1f206990e1bbd36098e4af3bc766c2f133017d8fae6601c9e06845aa8", "0x1d949b56871c93b9ba538effce403e184ff6cf649d26fe38179a0fee39b26485",
                "0x338a03514112afbf3e9a16963d79b73f1596daea2bf76f8f9c1db0effa5b04e7", "0x643861535bae1a76e432a9b322b0b780354420656c9877c448f7bf9215825417",
                "0x90372e7109480f7176a0202a9400e35c712b0449a760232c3f1f617689318ac7", "0xbb7faeb0948082216551c2f174ea2d92a7c2c065cfd5eb1d7b8e6084bd9e0c77",
                "0xfd880964eb8e8f7e67f91f410dd854906192554f7b8bf7aedbbb3ebc4e76011e", "0x209fe5d120ad45b9de452fa322f96a2189208eea651800eec7cb6eda0a26727e",
                "0x958680768394319d789c8ff94ed3cb4a7c47417eeeebca298bf24b9ba0b0b5bf", "0x93a17064cb3bfa8c8f697efa6670ee0c2a89f9e22b73db94ec4f00711004c1da",
                "0x93a17064cb3bfa8c8f697efa6670ee0c2a89f9e22b73db94ec4f00711004c1da", "0x2c806493e73655a68b3a3e6bd415e1615eee0badee7b568df474af6a537c2764",
                "0x4141ffc6a68aeb68b26bcdf1ab6d249042aa0795dc664d6eafc0e2c582286edc", "0xd77e1204db45319fa8468b445487cc6a561041d5565c6ac6bc6e1884c9bae5cf",
                "0x69fd1e9f7bae40054db010ced1c7877735dcafa2fb88bb2e3ab70ae73660cddf", "0x97dc4dd4734b7db284419413119605c0bae6eb9096cc8526078e9e62ce35bba1",
                "0x1f80b1fbab82488fcea702cad2ec8d4d772a02ecbfdd87e41f7e3fda6cab9634", "0x1750047d4adea3a591a87180b2bd906d9b02cee12f9c20a9c62700e1a414faeb",
                "0x656281b59f5095abebc0d4e5066b9cd043c7608d4db49cbf9204fcfe9a243c0c", "0x5d1a190bf5e58c6decbd4666c9ae40009e38191685f727d5f123bda3364b986a",
                "0x7350d7a9f3fa2eed7849d5379c63d11112aac0418981a453161a13cf3c64a1dc", "0x10e35115875122a4802ce279452716a5a193e04087902bf6c5a871556100a920",
                "0x0592eee9fc445a8e191610cfa10d53f97a9bdc854b8ff76251cce1cf026e7875", "0xb18d0d977101a4c30410a44c4759974a879f4effa4a7a52abc8cd36952b5d01d",
                "0xe29e7141b60a9cf8bfd8c1aec8885bd8511a040a99cbe4a3c79ad26c681af3cf", "0x3a42c0942e94fa5ba77d207ff24fab397b2e14d7504102ea12a0aa686734a4c0"]

    
    contract_addy = [] #empty list for all of the contract addresses          

    #https://ethereum.stackexchange.com/questions/32106/is-there-a-way-to-know-the-contract-creation-address-from-a-the-transaction
    for i in txn_hash: 
        contract_addy.append(web3.eth.getTransactionReceipt(i).contractAddress) #for each transaction, iterate through the list above and get the contract address 


    watching_contracts = [ContractEventDefinition("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0", "Sync")]
    
    for i in contract_addy:
        watching_contracts = watching_contracts.append(ContractEventDefinition(contract_addy[i], "Sync")) #for each contract address, create a contract event definition and store in watching_contracts



    flashloan_providers = [AaveFlashloanProvider()]
    arb_bot = Bot(watching_events=watching_contracts,
                  flashloan_providers=flashloan_providers)

    arb_bot.run()
