// contracts/FlashLoan.sol
// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;
pragma abicoder v2;
import "forge-std/console2.sol";

import {FlashLoanSimpleReceiverBase} from "@aave-v3/flashloan/base/FlashLoanSimpleReceiverBase.sol";
import {IPoolAddressesProvider} from "@aave-v3/IPoolAddressesProvider.sol";
import {IERC20} from "@openzeppelin/IERC20.sol";
import '@uniswap-v3/TransferHelper.sol';
import '@uniswap-v3/ISwapRouter.sol';
import '@uniswap-v3/IUniversalRouter.sol';
import '@uniswap-v2/UniswapV2Library.sol';


contract FlashLoan is FlashLoanSimpleReceiverBase {
    address payable owner;

    ISwapRouter public immutable swapRouter;

    uint24 public constant poolFee = 3000;

    address public constant DAI = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address public constant WETH9 = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address public constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;

    IUniversalRouter universalRouter = IUniversalRouter(0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD);

    constructor(address _addressProvider, address _swapRouter)
        FlashLoanSimpleReceiverBase(IPoolAddressesProvider(_addressProvider))
    {
        owner = payable(msg.sender);
        swapRouter = ISwapRouter(_swapRouter);
    }

    /// @notice swapInputMultiplePools swaps a fixed amount of DAI for a maximum possible amount of WETH9 through an intermediary pool.
    /// For this example, we will swap DAI to USDC, then USDC to WETH9 to achieve our desired output.
    /// @dev The calling address must approve this contract to spend at least `amountIn` worth of its DAI for this function to succeed.
    /// @param amountIn The amount of DAI to be swapped.
    /// @return amountOut The amount of WETH9 received after the swap.
    function swapExactInputMultihop(uint256 amountIn) public returns (uint256 amountOut) {
        // Assume this address already has amountIN

        // Approve the router to spend DAI.
        TransferHelper.safeApprove(DAI, address(swapRouter), amountIn);

        // Multiple pool swaps are encoded through bytes called a `path`. A path is a sequence of token addresses and poolFees that define the pools used in the swaps.
        // The format for pool encoding is (tokenIn, fee, tokenOut/tokenIn, fee, tokenOut) where tokenIn/tokenOut parameter is the shared token across the pools.
        // Since we are swapping DAI to USDC and then USDC to WETH9 the path encoding is (DAI, 0.3%, USDC, 0.3%, WETH9).
        ISwapRouter.ExactInputParams memory params =
            ISwapRouter.ExactInputParams({
                path: abi.encodePacked(DAI, poolFee, USDC, poolFee, WETH9, poolFee, DAI),
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: 0
            });

        // Executes the swap.
        amountOut = swapRouter.exactInput(params);
    }

    function customPathSwap(uint256 amountIn, address startToken, address[] calldata pathes) public returns (uint256 amountOut) {
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
        //
        // This contract now has the funds requested.
        // Your logic goes here.
        //

        console2.log("my balance", getBalance(asset));
//        swapExactInputMultihop(10000e18);

        // At the end of your logic above, this contract owes
        // the flashloaned amount + premiums.
        // Therefore ensure your contract has enough to repay
        // these amounts.

        // Approve the Pool contract allowance to *pull* the owed amount
        uint256 amountOwed = amount + premium;
//        console2.log("someargs", params);
        console2.log("amount owed", amountOwed);
        console2.log("my balance", getBalance(asset));
        IERC20(asset).approve(address(POOL), amountOwed);

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

        // Transfer `amountIn` of DAI to this contract.
//        TransferHelper.safeTransferFrom(DAI, msg.sender, address(this), 10000e18);


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