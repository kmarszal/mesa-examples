from mesa import Agent
from wolf_sheep.random_walk import RandomWalker


class Sheep(RandomWalker):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        # Random move
        self.random_move()
        living = True
    
        # Grass flag means that in this model sheep lose energy by moving and gain by eating grass 
        if self.model.grass:
            # After moving, sheep loses energy
            self.energy -= 1

            # Get all objects in this cell
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            # Get grass patch from the objects
            grass_patch = [obj for obj in this_cell
                           if isinstance(obj, GrassPatch)][0]
            # If patch is fully grown, eat it
            if grass_patch.fully_grown:
                # Get energy from eating patch
                self.energy += self.model.sheep_gain_from_food
                # Change status of patch
                grass_patch.fully_grown = False

            # If not enough energy, sheep dies
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
                living = False
        
        # TODO
        # If still alive, then maybe reproduce
        
            # Loose half of energy
            if self.model.grass:
                
            # Creating baby lamb with the same amount of energy
        



class Wolf(RandomWalker):
    '''
    A wolf that walks around, reproduces (asexually) and eats sheep.
    '''

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # Move randomly
        self.random_move()
        # Lose energy after moving
        self.energy -= 1
        
        
        x, y = self.pos
        # Get all objects in the cell
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        # Filter all the sheep from objects
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        # If there are sheep present, eat one
        if len(sheep) > 0:
            # Choose one sheep from the sheep on this cell
            sheep_to_eat = self.random.choice(sheep)
            # TODO
            # Kill the sheep
            
            
            # TODO
            # Gain energy from eating sheep
            

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(self.model.next_id(), self.pos, self.model,
                           self.moore, self.energy)
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    '''

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
