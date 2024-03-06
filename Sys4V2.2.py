
import networkx as nx
import random
import matplotlib.pyplot as plt
class Car:
    def __init__(self, current_node, destination, stations, charge_threshold = 0.5, battery_start = 40, route = None, route_boul = False):
        self.current_node = current_node
        self.battery = battery_start
        self.destination = destination
        self.battery_start = battery_start
        self.charge_threshold = charge_threshold
        self.route_boul = route_boul
        self.route = route
        self.stations = stations

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

 #   def update_battery(self, graph, route):
 #       next_node = route[1]
 #       weight = graph.get_edge_data(self.current_node, next_node)['weight']
  #      self.battery = self.battery - weight
  #      return self.battery

    def find_charger(self, graph):
        path_length = float('inf')
        closest_station = None
        print(self.stations)

        for station in stations:
                print(station.location)
                path_length_station = nx.shortest_path_length(graph, source=self.current_node, target=station.location, weight="weight")
                if path_length_station < path_length:
                    path_length = path_length_station
                    closest_station = station
        return closest_station.location



class Charging_station:
    def __init__(self, location, busy_state=True):
        self.location = location
        self.busy_state = busy_state



class TrafficSimulation:
    def __init__(self, graph, cars, stations):
        self.graph = graph
        self.cars = cars
        self.stations = stations

    def step(self):
        for car in self.cars:
            if car.current_node == car.destination:
                car.battery = car.battery_start
                print(car.battery)
                car.move(self.graph)
                car.route_boul = False

            elif car.battery > (car.battery_start * car.charge_threshold) and car.battery > 0 and car.route_boul == False:
                print(car.battery)
                car.move(self.graph)

            elif car.battery <= (car.battery_start * car.charge_threshold) and car.battery > 0 and car.route_boul == False:
                car.destination = car.find_charger(self.graph)
                print(car.destination)
                car.route = car.calculate_route(self.graph)
                car.route_boul = True

            elif car.battery <= (car.battery_start * car.charge_threshold) and car.battery > 0 and car.route_boul == True:
                print(car.route)
                car.move_to_des(self.graph, car.route)
                car.route.pop(0)
            else:
                print('car is empty')


def visualize(graph, cars, stations):
    plt.figure(figsize=(8, 6))
    pos = nx.spectral_layout(graph)

    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=10)

    for car in cars:
        nx.draw_networkx_nodes(graph, pos, nodelist=[car.current_node], node_color='red', node_size=50)
        nx.draw_networkx_nodes(graph, pos, nodelist=[car.destination], node_color='green', node_size=50)

    # Draw charging stations
    station_locations = [station.location for station in stations]
    nx.draw_networkx_nodes(graph, pos, nodelist=station_locations, node_color='yellow', node_size=50)

    plt.title('Traffic Simulation')
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

def place_stations():
    stations = []
    station_list = random.sample(range(1, 101), 5)
    for i in station_list:
        stations.append(Charging_station(i))

    return stations

stations = place_stations()
print(f'the stations are {stations}')

graph = graph()

cars = [Car(7, 40, stations)]
simulation = TrafficSimulation(graph, cars, stations)

for _ in range(40):
    simulation.step()
    print([(car.current_node, car.destination) for car in cars])
    #visualize(graph, cars, stations)

