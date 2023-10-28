// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.10;

import {Test, console2} from "forge-std/Test.sol";
import {FlashLoan} from "../src/Flashloan.sol";
import {IERC20} from "@openzeppelin/IERC20.sol";

contract FlashloanTest is Test {
    FlashLoan public fh;

    address immutable public poolProviderAddress = 0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e;
    address immutable public uniswapv3swapRouter = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
    address immutable public uniswapUniversalRouter = 0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD;

    IERC20 immutable public DAI = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F);
    IERC20 immutable public WETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    IERC20 immutable public USDT = IERC20(0xdAC17F958D2ee523a2206206994597C13D831ec7);

    function setUp() public {
        fh = new FlashLoan(poolProviderAddress, uniswapv3swapRouter);
    }

    function testOwner() public {
        console2.logAddress(address(this));
        assertEq(fh.getOwner(), address(this));
    }

    function testFlashloan() public {
        deal(address(DAI), address(fh), 10000e18 * 0.10); // how about a 10% fee

        fh.requestFlashLoan(address(DAI), 10000e18, "yoyoyoy");

        displayBalances(address(fh));
    }

    function displayBalances(address displayAddress) view public {
        console2.log("DAI balance", DAI.balanceOf(displayAddress));
        console2.log("WETH balance", WETH.balanceOf(displayAddress));
    }

    function testDirectSwap() public {

        deal(address(WETH), address(fh), 10e18);

        address[] memory poolPath = new address[](3);

        address dai_eth_pair = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;
        address dai_usdc_pair = 0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5;
        address usdc_eth_pair = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;

//        poolPath[0] = eth_usdt_pair;
        poolPath[0] = dai_eth_pair;
        poolPath[1] = dai_usdc_pair;
        poolPath[2] = usdc_eth_pair;

        fh.customPathSwap(10e18, address(WETH), poolPath);

        displayBalances(address(fh));
    }
}
