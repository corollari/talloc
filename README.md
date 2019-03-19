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

#### Transparency and auditability
This system lends itself quite well to full transparency and auditability. It should be possible to use commit-reveal schemes or time-locked secrets (see RSA's paper) to handle the auctions in such a way that any outside observer can verify the results.  
If the system were to be fully anonymous, convergence may be an issue as it would be possible for an attacker to fork the network by submitting bids right on the deadline. But, as all the actors are known and this attack requires a malevolent actor deliberately attacking the system, trying to pull this attack would just lead to having the attacker identified and punished. Therefore, this attack is extremely low priority or directly non-existent in the threat model of this system.  
If the system is anonymized in the future or people think that this issue is important enough to warrant the added complexity imposed by creating a solution for it, it could be solved by timestamping all messages using a centralized service or a blockchain.

### Optimization Algorithm
If we could model general happiness then we would be able to optimize the system for that. With that in mind we strive to create a cost function that models that with the intention of later using it to optimize the time-slot distribution using something like simulated annealing.

#### Example
A possible cost function could be something like `\sum_{professors}(hours that the professor should do - hours that the professor is doing in the current distribution)^2 + number of subjects a professor is teaching`, which, when minimized, would generate a distribution which is fair in the sense that each professor is working an amount of hours close to what it should be while the dispersion of subjects per professor is kept small.

#### Problems
- How do you pick the numerical constants used in the cost function?
  - A possible solution would be to use historical data to fit the constants to make the cost function as close to the conceptual cost function that has been used in previous allocations, that is, pick the constants which make the system generate allocations closest to the historical ones when fed historical data.
  - Another solution is to have users take a survey and infer these constants from the data obtained.
  - Yet another solution would be to have users develop their own cost functions, which would then be aggregated to construct the final cost function that would be optimized. That way each user could define what they believe is important when distributting time slots and the algorithm would take into account all the users opinions.
    - **Security:** Allowing users to set arbirtrary functions poses a huge security risk as they may create a function that makes the system ignore all the other users' functions or one that biases the system in their favor. A way to normalize these functions would need to be developed that makes all user-provided functions the same relevance.
    - **User Experience**: Having each user write their own cost function would lead to terrible UX as it would require a huge time sink, this could be alleviated by giving users several ways to define their functions with different degrees of freedom. A possible way of implementing these could be the following:
      - Users that don't want to spend much time on it could just pick among a set of three predefined functions
      - Users that want more freedom could pick the coeficients of the different terms of a predefined function (eg: pick `alpha` and `beta` in `alpha*low total number of hours + beta*time slots close to each other`)
      - Users that want even more control could write their own totally custom functions
- How will the function be?
  - Ask users for factors they think should be taken into account. Tuning their rellevance is inside the scope of the previous problem
  - The last solution proposed for the previous problem (have users define their own custom cost functions) would also solve this problem

#### Transparency and auditability
Making this system fully transparent and auditable would require using a fully deterministic optimization algorithm that has had its parameters (such as number of iterations) picked randomly. If these requirements are met, the result would be fully replicable and anyone should be able to verify the result by running the algorithms themself.

### Hybrid approaches
Other approaches to this problem can be created by mixing the two methods described so far, creating new systems like the following:
- Use vickrey auctions to obtain an initial distribution and then distribute the time-slots/subjects that haven't had any bidders using the optimization algorithm
- Use vickrey auctions to gauge player preferences (and also balance the system?) and then apply the optimization algorithm while taking into account these preferences (preference matching would be a part of the cost function)
