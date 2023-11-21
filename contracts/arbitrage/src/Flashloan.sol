// contracts/FlashLoan.sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;
pragma abicoder v2;
import "forge-std/console2.sol";

import {FlashLoanSimpleReceiverBase} from "@aave-v3/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import {IPoolAddressesProvider} from "@aave-v3/IPoolAddressesProvider.sol";
import {IERC20} from "@openzeppelin/IERC20.sol";
import '@uniswap-v3/TransferHelper.sol';
import '@uniswap-v2/UniswapV2Library.sol';


contract FlashLoan is FlashLoanSimpleReceiverBase {
    address payable owner;

    constructor(address _addressProvider)
        FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_addressProvider))
    {
        owner = payable(msg.sender);
    }

    function uniswapV2SwapTest(uint256 amountIn, address startToken, address[] memory pathes) public view returns (uint256 amountInNext) {
        // Assume this address already has amountIN
        require(pathes.length > 1, "Pathes array must have at least 2 elements");

        uint256 amountInNext = amountIn;
        for (uint i = 0; i < pathes.length; i++) {
            address pairAddress = pathes[i]; // Assuming the pathes array contains the addresses of LPs (pair contracts)
            IUniswapV2Pair pair = IUniswapV2Pair(pairAddress);
            address token0 = pair.token0();
            address token1 = pair.token1();

            (uint reserve0, uint reserve1,) = pair.getReserves();

            uint amountOut = 0;

            address tokenOut;

            if (startToken == token0) {
                amountOut = UniswapV2Library.getAmountOut(amountInNext, reserve0, reserve1);
                tokenOut = token1;
            } else {
                amountOut = UniswapV2Library.getAmountOut(amountInNext, reserve1, reserve0);
                tokenOut = token0;
            }

            // Approve the LP to spend the token
//            IERC20(startToken).transfer(pairAddress, amountInNext);

            // Swap
//            pair.swap(amountOut0, amountOut1, address(this), "");
            // Get the balance of the next token to be used as input for the next swap
            amountInNext = amountOut;
            startToken = tokenOut;
        }
        return amountInNext;
    }

    function uniswapV2Swap(uint256 amountIn, address startToken, address[] memory pathes) public returns (uint256 amountOut) {
        // Assume this address already has amountIN
        require(pathes.length > 1, "Pathes array must have at least 2 elements");

        uint256 amountInNext = amountIn;
        for (uint i = 0; i < pathes.length; i++) {
            address pairAddress = pathes[i]; // Assuming the pathes array contains the addresses of LPs (pair contracts)
            IUniswapV2Pair pair = IUniswapV2Pair(pairAddress);
            address token0 = pair.token0();
            address token1 = pair.token1();

            (uint reserve0, uint reserve1,) = pair.getReserves();

            uint amountOut0 = 0;
            uint amountOut1 = 0;

            address tokenOut;

            if (startToken == token0) {
                amountOut1 = UniswapV2Library.getAmountOut(amountInNext, reserve0, reserve1);
                tokenOut = token1;
            } else {
                amountOut0 = UniswapV2Library.getAmountOut(amountInNext, reserve1, reserve0);
                tokenOut = token0;
            }

            // Approve the LP to spend the token
            IERC20(startToken).transfer(pairAddress, amountInNext);
            uint amountInNextA = IERC20(tokenOut).balanceOf(address(this));

            // Swap
            pair.swap(amountOut0, amountOut1, address(this), "");
            // Get the balance of the next token to be used as input for the next swap
            amountInNext = IERC20(tokenOut).balanceOf(address(this));
            startToken = tokenOut;
        }

        return amountInNext;

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

    event Arb(uint256 initialAmount, uint256 finalAmount, address token);

    /**
        This function is called after your contract has received the flash loaned amount
     */
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {

        console2.log("starting balance with flashloan:", getBalance(asset));
        uint256 amountOwed = amount + premium;
        console2.log("flashloan amount owed:", amountOwed);

        // pre-determine that the flashloan amount is the swap initial amount
        (address decodeStartToken, address[] memory decodePathes) = fromBytes(params);
        uint256 finalTokenAmount = uniswapV2Swap(amount, asset, decodePathes);
        // Approve the Pool contract allowance to *pull* the owed amount

        console2.log("final_token_amount", finalTokenAmount);
        console2.log("my balance after swap:", getBalance(asset));
        IERC20(asset).approve(address(POOL), amountOwed);

        emit Arb(amount, finalTokenAmount, asset);

        return true;
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function requestFlashLoan(address _token, uint256 _amount, bytes calldata pathParams) public {
        address receiverAddress = address(this);
        address asset = _token;
        uint256 amount = _amount;
        uint16 referralCode = 0;

        POOL.flashLoanSimple(
            receiverAddress,
            asset,
            amount,
            pathParams,
            referralCode
        );
    }

    function getBalance(address _tokenAddress) public view returns (uint256) {
        return IERC20(_tokenAddress).balanceOf(address(this));
    }

    function withdraw(address _tokenAddress) external onlyOwner {
        IERC20 token = IERC20(_tokenAddress);
        token.transfer(msg.sender, token.balanceOf(address(this)));
    }

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only the contract owner can call this function"
        );
        _;
    }

    receive() external payable {}
}