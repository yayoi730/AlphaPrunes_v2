# CS4331 - Project 2 - Tournament Edition

## ORIGINAL PLAYER: BetaPrunes 
## NEW PLAYER: DeepDeltaPrunes

## Timeline of Improvements:

### Construction of SigmaPrunes
The agent, BetaPrunes, that we submitted for grading did not implement a fully-recursive minimax. Before making any improvements, we chose to redo our MiniMax algorithm to make it recursive and clean up the rest of our program as well, we dubbed it SigmaPrunes. Once we redid our MiniMax algorithm, the edited agent SigmaPrunes, kept beating our initial agent BetaPrunes.  

### Free-Choice Heuristic (SigmaPrunes V.2) 
Initially, upon having to choose a global board to make a move on, our agent chose randomly.
We implemented a heuristic that makes the agent choose a board that has it already has a 2
in a row in, after this our new agent consistently and quickly beat our old agent.

### Heuristic Sort Improvement (DeltaPrunes)
For our initial Heuristic sort in BetaPrunes we used a merge sort algorithm to sort the list of available moves that we were feeding to the minimax function. We were also sorting only the initial moves outside of the minimax algorithm. The first way we improved this was by placing where we sorted the available moves inside of the minimax recursion that way it appropriately sorts the moves at each depth. Next we changed the sorting algorithm from merge sort to quicksort. This drastically improved the time it took to sort all the moves and allowed the heuristic sorting to synergize well with the iterative deepening.

### Iterative Deepening (DeepeningPrunes) 
With the restructuring of our code, we had to redo our Iterative Deepening for MiniMax. It is the same as before (relies on a time constraint to break out of MiniMax), but now has a Max Depth of 5 as we found it works better if it’s not over predicting.

### DeepDelta Prunes
Alone, our Iterative-Deepening and Heuristic Sort Agent weren’t able to defeat our Free-Choice Heuristic agent (SigmaPrunes V.2), however, once we combined our Sorting and Iterative Deepening agents into one, DeepDelta, we saw that DeepDelta began to beat SigmaPrunes V.2. We studied this by running multiple tests which we graphed out.

What we noticed is amongst our agents, the agent that went second had the advantage. However, whenever DeepDeltaPrunes went first it had a higher chance of tying than SigmaPrunes. On the other hand, SigmaPrunes which had a higher chance of losing if it went first. As a result, we ultimately chose DeepDeltaPrunes over SigmaPrunes. 

Our results can be viewed in our attached charts. 
