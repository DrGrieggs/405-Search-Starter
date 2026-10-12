# Answers

Name:

## Parts 1–3

**Q1.** Is 450 miles the shortest distance from Arad to Bucharest? Why didn't breadth-first search care?

**Q2.** Delete the `is_cycle` check from depth-first search and run it again. What happens, and why?

**Q3.** What is the largest the frontier ever gets for breadth-first and for depth-first search on Arad to Bucharest?

**Q4.** Run `best_first_search(problem, lambda n: n.depth())`. Which of your earlier algorithms does it behave like?

**Q5.** Move the goal test in best-first search so it happens when a child is generated. Which route do you get, and why is it worse?

## Part 4: Choose your algorithm

### Problem A: The ambulance route

Algorithm chosen:

Why (2–3 sentences):

Route and total time:

What another algorithm gives, and why that's a problem for an ambulance:

### Problem B: The knight's journey

Algorithm chosen:

Why (2–3 sentences):

Number of moves and the squares visited:

### Problem C: The n queens

Algorithm chosen:

Why (2–3 sentences):

What would happen to memory with each of the other two algorithms:

## Reflection

**R1.** What is the only thing that differs between your three searches?

**R2.** What f(n) makes best-first search behave like breadth-first search, and why does breadth-first search still have its own FIFO version?

**R3.** Name a problem from this worksheet where returning the first solution found is fine, and explain why.

**R4.** Describe a problem of your own where best-first search with f(n) = path cost is clearly better than breadth-first search.
