import numpy as np
import random
from timeit import default_timer


class Knapsack:
    def __init__(self, knapsack_capacity, weights, values):
        self.knapsack_capacity = knapsack_capacity
        self.weights = np.array(weights)
        self.values = np.array(values)


class BruteForce(Knapsack):
    def __init__(self, knapsack_capacity, weights, values):
        super().__init__(knapsack_capacity, weights, values)

    def solve(self):
        st = default_timer()
        num_items = len(self.weights)
        best_combination = None
        best_value = 0

        # Перебор всех возможных комбинаций
        for i in range(2 ** num_items):
            binary_representation = format(i, f'0{num_items}b')
            current_combination = [int(bit) for bit in binary_representation]

            current_weight = np.dot(current_combination, self.weights)
            current_value = np.dot(current_combination, self.values)

            # Проверка, является ли текущая комбинация допустимым решением
            if current_weight <= self.knapsack_capacity and current_value > best_value:
                best_combination = current_combination
                best_value = current_value


        fn = default_timer()-st
        print("ПОЛНЫЙ ПЕРЕБОР")
        print("Время полного перебора: ", fn)
        return best_combination, best_value, fn


class GeneticAlgorithm(Knapsack):
    def __init__(self, knapsack_capacity, weights, values, population_size, mutation_probability, num_generations):
        super().__init__(knapsack_capacity, weights, values)
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.num_generations = num_generations
        self.extra_generations = 0

    # понаделать случайных смешных особей
    def create_individual(self, length):
        return np.random.randint(2, size=length)

    # оценка приспособленности
    def evaluate(self, individual):
        total_weight = np.sum(self.weights * individual)

        if total_weight <= self.knapsack_capacity:
            return np.sum(self.values * individual)
        else:
            return 0

    # выбор случайной особи для родительства
    def selection(self, population):
        fitness_values = [self.evaluate(individual) for individual in population]
        total_fitness = np.sum(fitness_values)

        if total_fitness == 0:
            # присваивает всем элементам одинаковую вероятность
            probabilities = np.ones(len(population)) / len(population)
        else:
            probabilities = []
            for fit_value in fitness_values:
                probabilities.append(fit_value / total_fitness)

        selected_index = np.random.choice(len(population), p=probabilities)
        return population[selected_index]

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(parent1) - 1)
        child = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
        return child

    def mutation(self, individual):
        mask = np.random.rand(len(individual)) < self.mutation_probability
        individual[mask] = 1 - individual[mask]

    def solve(self):
        st = default_timer()
        population = np.array([self.create_individual(len(self.weights)) for _ in range(self.population_size)])

        for generation in range(self.num_generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent1, parent2)
                self.mutation(child1)
                self.mutation(child2)
                new_population.append(child1)
                new_population.append(child2)
            population = np.array(new_population)

        # обработка случая, когда выходя из генетического алгоритма мы не имеем показателей приспособленности
        # отличных от нуля
        while self.evaluate(max(population, key=lambda i: self.evaluate(i))) == 0:
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.selection(population)
                parent2 = self.selection(population)
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent1, parent2)
                self.mutation(child1)
                self.mutation(child2)
                new_population.append(child1)
                new_population.append(child2)
            population = np.array(new_population)
            self.extra_generations += 1

        best_individual = max(population, key=lambda i: self.evaluate(i))
        fn = default_timer()-st
        print("ГЕНЕТИЧЕСКИЙ АЛГОРИТМ")
        print("Время: ", fn)
        print("Лучшая особь:", best_individual)
        print("Суммарный вес выбранных предметов:", np.sum(self.weights * best_individual))
        sum_value = np.sum(self.values * best_individual)
        print("Суммарная стоимость выбранных предметов:", np.sum(self.values * best_individual), '\n')

        return best_individual, sum_value, fn
