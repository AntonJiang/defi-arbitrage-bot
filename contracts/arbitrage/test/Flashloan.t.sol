// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.10;

import {Test, console2} from "forge-std/Test.sol";
import {FlashLoan} from "../src/Flashloan.sol";
import {IERC20} from "@openzeppelin/IERC20.sol";

contract FlashloanTest is Test {
    FlashLoan public fh;

    address immutable public poolProviderAddress = 0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e;

    IERC20 immutable public DAI = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F);
    IERC20 immutable public WETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    IERC20 immutable public USDT = IERC20(0xdAC17F958D2ee523a2206206994597C13D831ec7);

    function setUp() public {
        fh = new FlashLoan(poolProviderAddress);
    }

    function testOwner() public {
        console2.logAddress(address(this));
        assertEq(fh.getOwner(), address(this));
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

        poolPath[0] = dai_eth_pair;
        poolPath[1] = dai_usdc_pair;
        poolPath[2] = usdc_eth_pair;

        fh.uniswapV2Swap(10e18, address(WETH), poolPath);

        displayBalances(address(fh));
    }

    function testFlashloan() public {
        uint256 borrowAmount = 100000e18;
        uint256 slippage = borrowAmount * 2 / 10;
        uint256 flash_fee = borrowAmount * 5 / 10000;

        deal(address(DAI), address(fh), flash_fee + slippage); // how about a 10% fee

        address[] memory poolPath = new address[](3);

        address dai_eth_pair = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;
        address dai_usdc_pair = 0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5;
        address usdc_eth_pair = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;

        poolPath[0] = dai_eth_pair;
        poolPath[1] = usdc_eth_pair;
        poolPath[2] = dai_usdc_pair;

        bytes memory b = toBytes(address(DAI), poolPath);

        fh.requestFlashLoan(address(DAI), borrowAmount, b);

        displayBalances(address(fh));
    }

    function uniswapV2Swap(address startToken, address[] memory pathes) public {
        console2.log("", startToken);
        console2.log("p0", pathes[0]);
    }

    function testParams() public {
        address[] memory pathes = new address[](2);
        pathes[0] = 0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc;
        pathes[1] = 0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11;

        bytes memory b = toBytes(0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11, pathes);
        console2.logBytes(b);

        (address decodeStartToken, address[] memory decodePathes) = fromBytes(b);
        console2.log("decode A", decodeStartToken);

        for (uint i = 0; i < decodePathes.length; i++) {
            console2.log("decode P", decodePathes[i]);
        }
        console2.log("size P", decodePathes.length);
    }

    function fromBytes(bytes memory data) public pure returns (address startToken, address[] memory pathes) {
        require(data.length >= 20, "Data too short");

        // Extract the startToken
        uint160 num;
        assembly {
            num := mload(add(data, 20))
        }
        startToken = address(num);

        // Calculate the number of addresses in pathes
        uint256 numAddresses = (data.length - 20) / 20;
        pathes = new address[](numAddresses);

        // Extract each address
        for (uint256 i = 0; i < numAddresses; i++) {
            assembly {
                num := mload(add(add(data, 40), mul(i, 20)))
            }
            pathes[i] = address(num);
        }
    }


    function toBytes(address startToken, address[] memory pathes) public pure returns (bytes memory) {
        // Start with encoding startToken
        bytes memory data = abi.encodePacked(startToken);

        // Encode each address in pathes and concatenate
        for (uint i = 0; i < pathes.length; i++) {
            data = abi.encodePacked(data, pathes[i]);
        }

        return data;
    }



}
