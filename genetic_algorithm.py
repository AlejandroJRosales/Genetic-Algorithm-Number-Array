import random

genes_per_ch = 5
interval_max = 9
interval_min = 0
iterations = 100000
pop_keep = .8
pop_size = 20
prob_crossover = 0.9
prob_mutation = 0.15
tournament_size = 3
target = int(input("Target integer: "))


def generate_population():
    individuals = []
    for i in range(pop_size):
        chromosomes = []
        for c in range(genes_per_ch):
            chromosomes.append(random.randint(interval_min, interval_max))
        individuals.append(chromosomes)
    return individuals


def evaluate(population):
    pop_scores = []
    for individual in population:
        if len(individual) < genes_per_ch:
            missing_chr = genes_per_ch - len(individual)
            for i in range(missing_chr):
                individual.append(random.randint(interval_min, interval_max))
        score = 0
        for chromosomes in individual:
            score += chromosomes
        pop_scores.append(score)
    return pop_scores


def calc_fitness(pop_scores):
    pop_fitness = []
    for fitness in pop_scores:
        error = abs(target - fitness)
        pop_fitness.append(error)
    return pop_fitness


def select_fittest(population, pop_fitness):
    fitter_population = [population[pop_fitness.index(min(pop_fitness))]]
    for i in range(int(len(population) * pop_keep)):
        r = random.randint(0, len(pop_fitness) - 1)
        best = pop_fitness[r]
        best_index = population[r]
        for member in range(tournament_size):
            competitor_index = random.randint(0, len(pop_fitness) - 1)
            if pop_fitness[competitor_index] < best:
                best = pop_fitness[competitor_index]
                best_index = population[competitor_index]
        fitter_population.append(best_index)
    for a in range(len(population) - len(fitter_population)):
        chromosomes = []
        local_min = min(population[pop_fitness.index(min(pop_fitness))])
        local_max = max(population[pop_fitness.index(min(pop_fitness))])
        for c in range(0, genes_per_ch):
            chromosomes.append(random.randint(local_min, local_max))
        fitter_population.insert(random.randint(0, len(fitter_population)), chromosomes)
    return fitter_population


def crossover(population):
    for individual in range(int((len(population) - 2))):
        if random.random() <= prob_crossover:
            parent1 = population.pop(individual)
            parent2 = population.pop(individual + 1)
            r = random.randint(0, genes_per_ch)
            population.insert(random.randint(0, genes_per_ch), parent1[:r] + parent2[r:])
            population.insert(random.randint(0, genes_per_ch), parent2[:r] + parent1[r:])
    return population


def mutation(population):
    for individual in range(int((len(population) - 1))):
        if random.random() <= prob_mutation:
            ch = population.pop(individual)
            for i in range(0, 3):
                r = random.randint(0, 1)
                get_chr = ch.pop(random.randint(0, len(ch) - 1))
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
    for generation in range(0, iterations + 1):
        pop_scores = evaluate(population)
        pop_fitness = calc_fitness(pop_scores)
        if (generation % 10 == 0) | (target == pop_scores[pop_fitness.index(min(pop_fitness))]):
            best = min(pop_fitness)
            mode = max(set(pop_scores), key=pop_scores.count)
            worst = max(pop_fitness)
            display_best = pop_scores[pop_fitness.index(best)]
            display_worst = pop_scores[pop_fitness.index(worst)]
            print("[G %3d] score=(%4d, %4d, %4d): %r " %
                  (generation, display_best, mode, display_worst, population[pop_fitness.index(best)]))
            if target == pop_scores[pop_fitness.index(min(pop_fitness))]:
                break
        population = breed(select_fittest(population, pop_fitness))


if __name__ == "__main__":
    main()
