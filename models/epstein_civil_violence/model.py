import mesa
import math
from enum import Enum
class State(Enum):
    QUIET = 0
    ACTIVE = 1
    ARRESTED = 2
class Citizen(mesa.Agent):
    def __init__(self, model, vision, regime_legitimacy, 
                 arrest_prob_constant, threshold):
        super().__init__(model)
        self.vision = vision
        self.regime_legitimacy = regime_legitimacy
        self.arrest_prob_constant = arrest_prob_constant
        self.threshold = threshold
        self.hardship = self.random.random()
        self.risk_aversion = self.random.random()
        self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = 0
        self.state = State.QUIET
        self.jail_sentence = 0
    def update_arrest_probability(self):
        cops = 0
        actives = 1
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=self.vision
        )
        for agent in neighbors:
            if isinstance(agent, Cop):
                cops += 1
            elif isinstance(agent, Citizen) and agent.state == State.ACTIVE:
                actives += 1
        self.arrest_probability = 1 - math.exp(
            -self.arrest_prob_constant * round(cops / actives)
        )


    def step(self):
        if self.jail_sentence > 0:
            self.jail_sentence -= 1
            return
        self.update_arrest_probability()
        net_risk = self.risk_aversion * self.arrest_probability
        if self.grievance - net_risk > self.threshold:
            self.state = State.ACTIVE
        else:
            self.state = State.QUIET
        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=self.vision
        )
        empty = [c for c in neighbors if self.model.grid.is_cell_empty(c)]
        if empty:
            self.model.grid.move_agent(self, self.random.choice(empty))
class Cop(mesa.Agent):
    def __init__(self, model, vision):
        super().__init__(model)
        self.vision = vision

    def step(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=self.vision
        )
        actives = [a for a in neighbors 
                   if isinstance(a, Citizen) and a.state == State.ACTIVE]
        if actives:
            target = self.random.choice(actives)
            target.state = State.ARRESTED
            target.jail_sentence = self.random.randint(1, 5)
        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=self.vision
        )
        empty = [c for c in neighbors if self.model.grid.is_cell_empty(c)]
        if empty:
            self.model.grid.move_agent(self, self.random.choice(empty))    

class EpsteinModel(mesa.Model):
    def __init__(self, height=40, width=40, citizen_density=0.7,
                 cop_density=0.04, citizen_vision=7, cop_vision=7,
                 regime_legitimacy=0.8, arrest_prob_constant=2.3,
                 threshold=0.1, seed=None):
        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Quiet": lambda m: sum(
                    1 for a in m.agents 
                    if isinstance(a, Citizen) and a.state == State.QUIET),
                "Active": lambda m: sum(
                    1 for a in m.agents 
                    if isinstance(a, Citizen) and a.state == State.ACTIVE),
                "Arrested": lambda m: sum(
                    1 for a in m.agents 
                    if isinstance(a, Citizen) and a.state == State.ARRESTED),
            }
        )

        for cell in self.grid.coord_iter():
            _, pos = cell
            if self.random.random() < citizen_density:
                citizen = Citizen(self, citizen_vision, regime_legitimacy,
                                  arrest_prob_constant, threshold)
                self.grid.place_agent(citizen, pos)
            elif self.random.random() < cop_density:
                cop = Cop(self, cop_vision)
                self.grid.place_agent(cop, pos)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)


# Run it
model = EpsteinModel(seed=42)
for i in range(10):
    model.step()

df = model.datacollector.get_model_vars_dataframe()
print(df)