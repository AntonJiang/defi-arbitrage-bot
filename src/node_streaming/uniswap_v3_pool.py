from src.node_streaming import ContractEventDefinition
from src.node_streaming.web3_pool import Web3Pool


class UniswapV3PoolFinder():

    def __init__(self, w3: Web3Pool):
        self.w3 = w3

    def find_pool_manual(self) -> list[ContractEventDefinition]:
        return [
        ContractEventDefinition("0xcbcdf9626bc03e24f779434178a73a0b4bad62ed", "Swap"),
            ContractEventDefinition("0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", "Swap"),
            ContractEventDefinition("0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8", "Swap"),
            ContractEventDefinition("0x4e68ccd3e89f51c3074ca5072bbac773960dfa36", "Swap"),
            ContractEventDefinition("0x4585fe77225b41b697c938b018e2ac67ac5a20c0", "Swap"),
            ContractEventDefinition("0x7379e81228514a1d2a6cf7559203998e20598346", "Swap"),
            ContractEventDefinition("0x11b815efb8f581194ae79006d24e0d814b7697f6", "Swap"),
            ContractEventDefinition("0x109830a1aaad605bbf02a9dfa7b0b92ec2fb7daa", "Swap"),
            ContractEventDefinition("0xa6cc3c2531fdaa6ae1a3ca84c2855806728693e8", "Swap"),
            ContractEventDefinition("0xc5c134a1f112efa96003f8559dba6fac0ba77692", "Swap"),
            ContractEventDefinition("0x1d42064fc4beb5f8aaf85f4617ae8b3b5b8bd801", "Swap"),
            ContractEventDefinition("0xe8c6c9227491c0a8156a0106a0204d881bb7e531", "Swap"),
            ContractEventDefinition("0x40e629a26d96baa6d81fae5f97205c2ab2c1ff29", "Swap"),
            ContractEventDefinition("0xc2e9f25be6257c210d7adf0d4cd6e3e881ba25f8", "Swap"),
            ContractEventDefinition("0xf4c5e0f4590b6679b3030d29a84857f226087fef", "Swap"),
            ContractEventDefinition("0x3afdc5e6dfc0b0a507a8e023c9dce2cafc310316", "Swap"),
            ContractEventDefinition("0x058d79a4c6eb5b11d0248993ffa1faa168ddd3c0", "Swap"),
            ContractEventDefinition("0x4a80e5796794153f3f3b5c5ed45a15ab4c548738", "Swap"),
            ContractEventDefinition("0x01a8227d4e7c3068ad1000c97a059af5c5fa3476", "Swap"),
            ContractEventDefinition("0x510100d5143e011db24e2aa38abe85d73d5b2177", "Swap"),
            ContractEventDefinition("0x60594a405d53811d3bc4766596efd80fd545a270", "Swap"),
            ContractEventDefinition("0xa3f558aebaecaf0e11ca4b2199cc5ed341edfd74", "Swap"),
            ContractEventDefinition("0x381fe4eb128db1621647ca00965da3f9e09f4fac", "Swap"),
            ContractEventDefinition("0xa4e0faa58465a2d369aa21b3e42d43374c6f9613", "Swap"),
            ContractEventDefinition("0x71d091e35abbd51b46db179184684633581d1816", "Swap"),
            ContractEventDefinition("0xe72377ae353edc1d07f6c0be34969a481d030d19", "Swap"),
            ContractEventDefinition("0x2e8daf55f212be91d3fa882cceab193a08fddeb2", "Swap"),
            ContractEventDefinition("0x99132b53ab44694eeb372e87bced3929e4ab8456", "Swap"),
            ContractEventDefinition("0xc1cd3d0913f4633b43fcddbcd7342bc9b71c676f", "Swap"),
            ContractEventDefinition("0x290a6a7460b308ee3f19023d2d00de604bcf5b42", "Swap"),

        ]