# Rumour Spread Model

## What this model does:
I created a simple simulation of how a rumour spreads through a school of 20 students. 
Only one student knows the rumour at the start of each day and any student who 
knows the rumour tells it to one random classmate.

## Mesa features used
- `mesa.Agent` — each student is an agent with a "heard_rumour" property
- `mesa.Model` — the school contains all students
- `step()` — what each agent (student in this case)does every day
- `shuffle_do()` — randomizes the order agents act each day
- `seed` — controls randomness so results are reproducible

## What I learned 
- How agents and models connect in Mesa
- What `self` means in Python and why it matters
- How `super().__init__()` registers an agent with Mesa
- How changing the seed changes the simulation results completely
- How information spreads exponentially — more spreaders = faster spread

## What was hard for me
- Understanding indentation errors in Python (i sometimes get confused in it)
- Figuring out the difference between `seed=42` and `seed=None`
- Understanding why `shuffle_do` exists instead of just looping it

## Results
```
seed=42: Day 1: 2, Day 2: 4, Day 3: 7, Day 4: 11, Day 5: 18
seed=99: Day 1: 4, Day 2: 10, Day 3: 13, Day 4: 20, Day 5: 20
```
Different seeds produce different spread patterns with the same rules.