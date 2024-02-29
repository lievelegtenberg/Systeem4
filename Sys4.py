import networkx as nx
import random
import matplotlib.pyplot as plt


class Car:
    def __init__(self, current_node, destination, charge_threshold = 1, battery_start = 40, route = None, route_boul = False):
        self.current_node = current_node
        self.battery = battery_start
        self.destination = destination
        self.battery_start = battery_start
        self.charge_threshold = charge_threshold
        self.route_boul = route_boul
        self.route = route

    def move(self, graph):
        neighbors = list(graph.neighbors(self.current_node))
        next_node = random.choice(neighbors)
        self.battery = self.battery - self.calculate_weight(graph, next_node)
        self.current_node = next_node

    def move_to_des(self, graph, route):
        next_node = route[1]
        self.battery = self.battery - self.calculate_weight(graph, next_node)
        self.current_node = next_node
    def calculate_weight(self, graph, next_node):
       weight = graph.get_edge_data(self.current_node, next_node)['weight']
       return(weight)

    def calculate_route(self, graph):
        return nx.shortest_path(graph, source=self.current_node, target=self.destination, weight='weight',
                                method='dijkstra')

    def update_battery(self, graph, route):
        next_node = route[1]
        weight = graph.get_edge_data(self.current_node, next_node)['weight']
        self.battery = self.battery - weight
        return self.battery

class TrafficSimulation:
    def __init__(self, graph, cars):
        self.graph = graph
        self.cars = cars

    def step(self):
        for car in self.cars:
            if car.current_node == car.destination:
                car.battery = car.battery
                car.move(self.graph)
            elif car.battery > (car.battery_start * car.charge_threshold) and car.battery > 0 and car.route_boul == False:
                # car.update_battery(self.graph, route)
                print(car.battery)
                car.move(self.graph)

            elif car.battery <= (car.battery_start * car.charge_threshold) and car.battery > 0 and car.route_boul == False:
                car.route = car.calculate_route(self.graph)
                car.route_boul = True
                print(car.route)

            elif car.battery <= (car.battery_start * car.charge_threshold) and car.battery > 0 and car.route_boul == True:
                print(car.route)
                car.move_to_des(self.graph, car.route)
                car.route.pop(0)
            else:
                print('car is empty')


def visualize(graph, cars):
    plt.figure(figsize=(5, 3))
    pos = nx.spectral_layout(graph)
    nx.draw(graph, pos, with_labels=False, node_color='lightblue', node_size=10)  # Draw the network graph
    for car in cars:
        nx.draw_networkx_nodes(graph, pos, nodelist=[car.current_node], node_color='red', node_size=50)
        nx.draw_networkx_nodes(graph, pos, nodelist=[car.destination], node_color='green', node_size=50)

    plt.show()


def graph():
    g = nx.Graph()
    x_size = 10
    y_size = 10
    g.add_nodes_from(range(x_size * y_size))

    for i in range(x_size * y_size):
        if (i + 1) % x_size != 0:  # Check if not last collum
            g.add_edge(i, i + 1, weight=random.randint(1, 4))
        if i + x_size < x_size * y_size:  # Check if not last row
            g.add_edge(i, i + x_size, weight=random.randint(1, 4))

    return g


graph = graph() 

cars = [Car(7, 40)]
simulation = TrafficSimulation(graph, cars)

for _ in range(20):
    simulation.step()
    print([(car.current_node, car.destination) for car in cars])
    visualize(graph, cars)

