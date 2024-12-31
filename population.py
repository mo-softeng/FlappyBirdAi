import config
import player
import math 
import species
import operator
import pygame

class Population:
    def __init__(self, size):
        self.players = []
        self.size = size
        self.generations = 1
        self.species = []
        for ply in range(self.size):
            self.players.append(player.Player()) # append n player objects based on size 
    def natural_selection(self):
        print('SPECIATE')
        self.speciate()

        print('CALCULATE FITNESS')
        self.calculate_fitness()

        print('KILL EXTINCT')
        self.kill_extinct_species()

        print('KILL STALE')
        self.kill_stale_species()

        print('SORT BY FITNESS')
        self.sort_species_by_fitness()

        print('CHILDREN FOR NEXT GEN')
        self.next_gen()
    
    def speciate(self):
        for s in self.species:
            s.players = []
        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        species_bin = []
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    def next_gen(self):
        children = []

        # Clone of champion is added to each species
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generations += 1

    def kill_stale_species(self):
        player_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)

    def update_live_players(self):
        for ply in self.players:
            if ply.alive: 
                ply.look()
                ply.think()
                ply.draw(config.window) 
                ply.update(config.ground)
        
    def extinct(self):
        extinct = True
        for ply in self.players:
            if ply.alive:
                extinct = False
        return extinct
    def show_generation(self, window):
        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(F"Generation: {self.generations}", True, (255, 255, 255))  # White text
        window.blit(text_surface, (0, 0))