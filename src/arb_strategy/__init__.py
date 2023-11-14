import abc

from src.data_processing.trading_path import TradingPath


class ArbStrategy(abc.ABC):

    starting_tokens: list[str]

    def __init__(self):
        self.starting_tokens = self.get_flashloan_tokens()

    def get_flashloan_tokens(self) -> list[str]:
        """
        returns a list of flashloanable tokens, these tokens needs to be the start of the path
        :return:
        """
        # TODO (hard code @andy)
        pass

    @abc.abstractmethod
    def compute_optimal_path(self, trading_paths: list[TradingPath]):
        pass


class BruteForceArbStrategy(ArbStrategy):
    """
    TODO
    """

    def compute_optimal_path(self, trading_paths: list[TradingPath]):
        #this assumes trading paths is a list of all possible trading paths??? unless each TradingPath is A->B and not possibly A->B->C which would be find just implement combinations as a later function
        
        #first get the optimal arbitrage path while gating out the non flashloanable paths 
        #should be gated here because this is where we get the flash loan information 
        
        flash = get_flashloan_tokens(self) #figure out which tokens are flashloanable
        arbitrage_profits = compute_all_profit(self, trading_paths) #figure out what the profits are per trading path, i wanted this is as a list of lists but it could be an atrribute
        
        max_profit = arbitrage_profits[0] #set up for loop to find maximal profit
        
        for i in arbitrage_profits: 
            if i.first_token in flash & i.last_token in flash: #flash loan gate 
                if i[1] >> max_profit[1]: 
                    max_profit = i
        
        optimal_path =  max_profit[0]

        #then figure out the optimal hyperparameters/gates 
            #idk how to know how much to flashloan 
            #use gas class to figure out how much to gas 
            #add any extra information needed for the simulation module onto optimal path
        
        return optimal_path


    def compute_all_profit(self, trading_paths: list[TradingPath]):
        #this should return all the profits of all the arbitrage paths 

        all_combinations = combinations(self, trading_paths)
        #and then use all_combinations instead of trading paths in the for loop 

        profits = []
        for i in all_combinations: 
            profits[i] = [trading_paths[i], trading_paths[i].calculate_price] #not sure if this is the correct way to calculate price
            

        return profits 


    def combinations(self, trading_paths: list[TradingPath]):
        if trading_paths: 
            result = combinations(trading_paths[:-1]) 
            return result + [c + [trading_paths[-1]] for c in result] 
        else: 
            return [[]] 
