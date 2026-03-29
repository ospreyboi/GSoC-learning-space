##What the model simulates:

this model simulates, a society where citizens decide whether to rebel against there government or not.this is based on how much they are being troubled and this also determines how likely the citizens will be arrested.this model is trying to replicate how unrests get started and how they are suppresed.which sometimes can be balanced and sometimes explode into chaos.

##MESA features used:

1.mesa.Agent — two agent types: Citizen and Cop
2.mesa.space.SingleGrid — a grid where agents move around
3.mesa.DataCollector — tracks how many citizens are Quiet, Active, or Arrested each step
4.shuffle_do — randomizes which agent acts first each step
5.State enum — cleanly represents citizen states

##What the output means:

1.Step 0: 597 citizens are quiet, 520 citizens are actively rebelling, 14 people are arrested — most citizens start quiet
2.By Step 2: people actively rebelling increase as the movement spreads.
3.By Step 5-9: system reaches equilibrium around 546 get quiet, 530 people get active, 50 get arrested.
This means cops can suppress but never fully stop rebellion — a realistic dynamic

##What I found interesting:

Small changes in regime legitimacy dramatically change the number of rebels
The system reaches equilibrium naturally without being programmed to do specifically that,it emerges from individual agent decisions.
The same math from Epstein's 2002 research paper produces realistic looking civil unrest dynamics