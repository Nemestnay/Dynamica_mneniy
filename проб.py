import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, capital, desire_to_leave, threshold, stubbornness):
        self.capital = capital
        self.desire_to_leave = desire_to_leave
        self.threshold = threshold
        self.stubbornness = stubbornness

    def update_desire(self, neighbors):
        total_desire = sum(neighbors) / len(neighbors)
        self.desire_to_leave = total_desire

def create_agents(num_agents):
    agents = []
    for _ in range(num_agents):
        capital = random.expovariate(0.1)  * 1000000 # Генерация капитала по экспоненциальному распределению
        desire_to_leave = random.random()  # Желание уехать из России от 0 до 1
        threshold = random.uniform(0.4, 1)  # Пороговое значение для уезда
        stubbornness = random.uniform(0, 0.3)   #Коэффициент упрямости
        agent = Agent(capital, desire_to_leave, threshold, stubbornness)
        agents.append(agent)

    return agents


def create_graph(agents, num_influencers=10):
    G = nx.Graph()
    for i, agent in enumerate(agents):
        if i < num_influencers:
            G.add_node(i, type="influencer", capital=agent.capital, desire_to_leave=agent.desire_to_leave,
                       threshold=agent.threshold)
        else:
            G.add_node(i, type="agent", capital=agent.capital, desire_to_leave=agent.desire_to_leave,
                       threshold=agent.threshold)

    for i in range(num_influencers):
        G.add_edges_from([(i, j) for j in range(num_influencers, len(agents))])

    for i in range(num_influencers):
        family_size = random.randint(1, 10)
        family_members = random.sample(range(num_influencers), family_size)
        for member in family_members:
            G.add_edge(i, member)

    for i in range(num_influencers, len(agents)):
        family_size = random.randint(1, 10)
        family_members = random.sample(range(num_influencers, len(agents)), family_size)
        G.add_edges_from([(i, member) for member in family_members])

    return G


def simulate_migration(agents, graph):
    num_left_country = 0
    for agent in agents:
        neighbors = [agents[j].desire_to_leave for j in graph.neighbors(agents.index(agent))]
        agent.update_desire(neighbors)
        agent.capital *= (1.1) ** (1/12)  # Увеличение капитала на 10% годовых ежемесячно
        if agent.capital > 10000000 and agent.desire_to_leave >= agent.threshold + agent.stubbornness:
            num_left_country += 1
            agent.desire_to_leave = 1
    return num_left_country

def visualize_migration(num_left_country_history):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(num_left_country_history)), num_left_country_history, marker='o', linestyle='-')
    plt.xlabel('Month')
    plt.ylabel('Number of Agents Left Country')
    plt.title('Migration Dynamics')
    plt.grid(True)
    plt.show()

def main(num_agents, num_month):
    agents = create_agents(num_agents)
    graph = create_graph(agents)
    num_left_country_history = []
    for month in range(num_month):
        num_left_country = simulate_migration(agents, graph)
        num_left_country_history.append(num_left_country)
        if num_left_country > 0:
            print(f'{num_left_country} agents left the country on month {month + 1}.')
            print(f'{num_left_country} agents left the country on month {month + 1}.')

    visualize_migration(num_left_country_history)

if __name__ == "__main__":
    main(num_agents=1000, num_month=12* 100)
