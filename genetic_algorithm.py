import random


iterations = 1000
pop_size = 500
tournament_size = 3
pop_keep = .6
prob_crossover = 0.9
prob_mutation = 0.15
target = [random.randint(0, 100) for i in range(10)]
genes_per_ch = len(target)
interval_max = max(target)
interval_min = min(target)


def generate_population():
    individuals = []
    for i in range(0, pop_size):
        chromosomes = []
        for c in range(0, genes_per_ch):
            chromosomes.append(random.randint(interval_min, interval_max))
        individuals.append(chromosomes)
    return individuals


def calc_fitness(population):
    fitness_scores = []
    for individual in range(len(population)):
        if len(population[individual]) < genes_per_ch:
            missing_chr = genes_per_ch - len(population[individual])
            for i in range(0, missing_chr):
                individual_index = population[individual]
                individual_index.append(random.randint(interval_min, interval_max))
        fitness = 0
        for i in range(genes_per_ch):
            place = population[individual]
            difference = abs(target[i] - place[i])
            fitness += difference
        fitness_scores.append(fitness)
    return fitness_scores


def select_fittest(population, fitness_scores):
    fitter_population = [population[fitness_scores.index(min(fitness_scores))]]
    for i in range(0, int(len(population) * pop_keep)):
        r = random.randint(0, len(fitness_scores) - 1)
        best = fitness_scores[r]
        best_ch = population[r]
        for member in range(0, tournament_size):
            competitor_index = random.randint(0, len(fitness_scores) - 1)
            if fitness_scores[competitor_index] < best:
                best = fitness_scores[competitor_index]
                best_ch = population[competitor_index]
        fitter_population.append(best_ch)
    for a in range(len(population) - len(fitter_population)):
        chromosomes = []
        for c in range(0, genes_per_ch):
            chromosomes.append(random.randint(interval_min, interval_max))
        fitter_population.append(chromosomes)
    return fitter_population


def crossover(population):
    for individual in range(int((len(population) - 2))):
        if random.random() <= prob_crossover:
            parent1 = population.pop(individual)
            parent2 = population.pop(individual + 1)
            r = random.randint(0, genes_per_ch)
            population.insert(individual, parent1[:r] + parent2[r:])
            population.insert(individual + 1, parent2[:r] + parent1[r:])
    return population


def mutation(population):
    for individual in range(int((len(population) - 1))):
        if random.random() <= prob_mutation:
            ch = population.pop(individual)
            for i in range(0, 3):
                r = random.randint(0, 1)
                get_chr = ch.pop(random.randint(0, genes_per_ch))
                mutate = 1
                if r == 0:
                    if get_chr >= interval_min + mutate:
                        ch.append(get_chr - mutate)
                    else:
                        break
                else:
                    if get_chr <= interval_max - mutate:
                        ch.append(get_chr + mutate)
                    else:
                        break
            population.append(ch)
        return population


def breed(population):
    return mutation(crossover(population))


def main():
    population = generate_population()
    fitness_scores = []
    for generation in range(0, iterations + 1):
        fitness_scores = calc_fitness(population)
        if generation % 10 == 0:
            best = min(fitness_scores)
            mode = max(set(fitness_scores), key=fitness_scores.count)
            worst = max(fitness_scores)
            display_best = fitness_scores[fitness_scores.index(best)]
            display_worst = fitness_scores[fitness_scores.index(worst)]
            print("[G %3d] score=(%4f, %4f, %4f): %r" %
                  (generation, display_best, mode, display_worst, population[fitness_scores.index(best)]))
            if display_best == 0:
                break
        population = breed(select_fittest(population, fitness_scores))
    best = min(fitness_scores)
    display_best = population[fitness_scores.index(best)]
    print("\n\nT:", target)
    print("A:", display_best)


if __name__ == "__main__":
    main()
