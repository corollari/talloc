# talloc
> Time Alloc: Optimizing time-slots allocations in a timetable

## Possible systems
### Vickrey auctions
- Players bid on items using their time
- The person who wins the auction gets the item paying the second  
- Game-theoretical optimum allocation (players are incentivized to bid the real price an item is worth for them & the whole system optimizes the allocations so that players get the best outcome based on what they prefer)
#### Problems
- When are auctions done?
  - All the auctions are done concurrently then unassigned items are auctioned in other auction rounds
    - Example
      - Auctions for A, B, C, D
      - Nobody bids on B, C
      - Auctions for B, C
      - ...
    - Problems
      - Not optimal as players have to place all their bids at the same time, therefore locking currency in their bids which ends up causing inefficient allocations when they don't win auctions. Vickrey auctions are only optimal when no auctions are held at the same time.
      - Example
        - Player 1 thinks item A is worth 10, item B is worth 4. He has 10 coins.
        - Player 2 thinks item A is worth 11, item B is worth 0. He has 11 coins.
        - Player 3 thinks item A is worth 0, item B is worth 3. He has 3 coin.
        - Player 1 as a rational agent bids 2.857142857 on B and 7.142857143 on A.
        - Player 2 bids 11 on A.
        - Player 3 bids 3 on B.
        - Player 2 gets B and player 3 gets A.
        - The optimal allocation would have been for Player 1 to get item B and for Player 2 to get item A.
        - Conclusion: The final allocation is not optimal.
  - All auctions are done sequentially
    - An optimal distribution is reached -> optimal outcome is achieved according to game theory.
    - Problems:
      - There's over 500 items to auction in our problem, this system is not viable as it would take too long to auction them all.
  - Auctions are done in batches
    - Mixes the concurrent and sequential approaches
    - How?
      - Use historical data to predict which players are interested in which items
      - Bundle auctions in batches minimizing the amount of items each player is interested in (so optimally a batch would only contain one item that each player would be interested in, these items could be different for each player)
      - Auctions the items in batches (all auctions inside a batch are auctioned concurrently and batches are done sequentially)

### System to be optimized
If we could model general happiness then we would be able to optimize the system for that. With that in mind we strive to create a cost function that models that with the intention of later using it to optimize the time-slot distribution using something like simulated annealing.
#### Example
A possible cost function could be something like `\sum_{professors}(hours that the professor should do - hours that the professor is doing in the current distribution)^2 + number of subjects a professor is teaching`, which, when minimized, would generate a distribution which is fair in the sense that each professor is working an amount of hours close to what it should be while the dispersion of subjects per professor is kept small.
#### Problems
- How do you pick the numerical constants used in the functions?
  - A possible solution would be to use historical data to fit the constants to make the cost function as close to the conceptual cost function that has been used in previous allocations, that is, pick the constants which make the system generate allocations closest to the historical ones when fed historical data.
