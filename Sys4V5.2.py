import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Car:
    def __init__(self, current_node, destination, stations, destination_list, total_distance=0, charger=None,
                 charge_threshold=0.5, battery_start=300, times_charged = 0, route=None, charging_boul=False, finised = True ):
        self.current_node = current_node
        self.battery = battery_start
        self.destination = destination
        self.battery_start = battery_start
        self.charge_threshold = charge_threshold
        self.charging_boul = charging_boul
        self.route = route
        self.charger = charger
        self.stations = stations
        self.destination_list = destination_list
        self.total_distance = total_distance
        self.finised = finised
        self.times_charged = times_charged

    #def move(self, graph):
    #    neighbors = list(graph.neighbors(self.current_node))
    #    next_node = random.choice(neighbors)
    #    self.battery = self.battery - self.calculate_weight(graph, next_node)
    #     self.total_distance = self.total_distance + self.calculate_weight(graph, next_node)
    #     self.current_node = next_node
    #     print(self.destination_list)

    def move_to_des(self, graph, route):
        if not route:
            print("Route is empty")
            return
        next_node = route[1]
        self.battery = self.battery - self.calculate_weight(graph, next_node)
        self.total_distance = self.total_distance + self.calculate_weight(graph, next_node)
        self.current_node = next_node

    def calculate_weight(self, graph, next_node):
        weight = graph.get_edge_data(self.current_node, next_node)['weight']
        return (weight)

    def calculate_route(self, graph, destination_node):
        return nx.shortest_path(graph, source=self.current_node, target=destination_node, weight='weight',
                                method='dijkstra')

    def find_charger(self, graph):
        path_length = float('inf')
        closest_station = None

        for station in stations:
            path_length_station = nx.shortest_path_length(graph, source=self.current_node, target=station.location,
                                                          weight="weight")
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
        self.stations = stations  #the nodes where the car can charge

    def step(self):
        for car in self.cars:
            if len(car.destination_list) == 0:
                break

            elif car.current_node == car.destination and car.current_node ==car.charger: #in case the destination is same as charger
                print('charger and destination are same')
                car.charging_boul = False
                car.times_charged = car.times_charged + 1
                car.destination_list = car.destination_list[1:]
                if len(car.destination_list) == 0:
                    break
                else:
                    car.destination = car.destination_list[0]
                    car.route = car.calculate_route(self.graph, car.destination)
                    car.move_to_des(self.graph, car.route)
                    car.route.pop(0)

            elif car.current_node == car.destination and car.charging_boul == False:  #Car is at destination
                car.destination_list = car.destination_list[1:]
                if len(car.destination_list) == 0:
                    break

                else:
                    car.destination = car.destination_list[0]
                    car.route = car.calculate_route(self.graph, car.destination)
                    car.move_to_des(self.graph, car.route)
                    car.route.pop(0)

            elif car.battery >= (car.battery_start * car.charge_threshold) and car.battery > 0 and car.charging_boul == False:  #Car moves to destination
                car.move_to_des(self.graph, car.route)
                car.route.pop(0)

                ### MOVING TO CHARGER ##

            elif car.current_node == car.charger and car.charging_boul == True:  #Car is at charger
                car.battery = car.battery_start
                car.charging_boul = False
                car.times_charged = car.times_charged + 1
                car.destination = car.destination_list[0]
                car.route = car.calculate_route(self.graph, car.destination)
                car.move_to_des(self.graph, car.route)
                car.route.pop(0)

            elif car.battery <= (car.battery_start * car.charge_threshold) and car.battery > 0 and car.charging_boul == False:
                car.charger = car.find_charger(self.graph)
                car.route = car.calculate_route(self.graph, car.charger)
                car.charging_boul = True

            elif car.battery <= (
                    car.battery_start * car.charge_threshold) and car.battery > 0 and car.charging_boul == True:
                car.move_to_des(self.graph, car.route)
                car.route.pop(0)
            else:
                car.finised = False


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


def set_up_graph():
    g = nx.Graph()
    x_size = 10
    y_size = 10
    g.add_nodes_from(range((x_size * y_size)))

    for i in range((x_size * y_size)):
        if (i + 1) % x_size != 0:  # Check if not last collum
            g.add_edge(i, i + 1, weight=random.randint(10, 50))
        if i + x_size < x_size * y_size:  # Check if not last row
            g.add_edge(i, i + x_size, weight=random.randint(10, 50))

    return g


def place_stations(amout_stations):
    stations = []
    station_list = random.sample(range(1, 100), amout_stations)
    for i in station_list:
        stations.append(Charging_station(i))

    return stations


import numpy as np

# Create an empty DataFrame to store results
results_all_df = pd.DataFrame(
    columns=['Run', 'Total Distance', 'Finished', 'Times Charged', 'Battery Threshold', 'Num Stations'])

# Define the range of battery thresholds
battery_thresholds = np.linspace(0.4, 0.5, 3)

# Define the range of numbers of stations
num_stations_range = range(20, 20)  # Adjust range as needed

#for num_stations in num_stations_range:
#    print(f"Running simulations with {num_stations} stations")

for threshold in battery_thresholds:
    print(f"Running simulations with battery threshold: {threshold}")
    results_df = pd.DataFrame(columns=['Run', 'Total Distance', 'Finished', 'Times Charged'])

    threshold = 0.4
    num_stations = 20
    for run in range(200):  # Change the range to the number of simulations you want
        print(f'the run is: {run}')
        stations = place_stations(num_stations)
        graph = set_up_graph()
        destinations = [1, 80, 45, 10, 99, 30, 22, 56, 1, 80, 45, 10, 99, 30, 22, 56]
        cars = [Car(1, 1, stations, destinations, charge_threshold=threshold)]
        simulation = TrafficSimulation(graph, cars, stations)

        for _ in range(4000):
            simulation.step()

        total_distance = cars[0].total_distance  # Assuming only one car in the simulation
        empty = cars[0].finised
        times_charged = cars[0].times_charged
        results_df = pd.concat([results_df, pd.DataFrame(
            {'Run': [run + 1], 'Total Distance': [total_distance], 'Finished': [empty],
             'Times Charged': [times_charged], 'Battery Threshold': [threshold], 'Num Stations': [num_stations]})])

    results_all_df = pd.concat([results_all_df, results_df])

# Print the DataFrame with results
print(results_all_df)

# Plotting
# for threshold in battery_thresholds:
#     for num_stations in num_stations_range:
df = results_all_df[
    (results_all_df['Battery Threshold'] == threshold) & (results_all_df['Num Stations'] == num_stations)]

# Create a scatter plot
plt.figure(figsize=(8, 6))

# Extracting data from the DataFrame
x = df['Total Distance']
y = df['Times Charged']
finished = df['Finished']

# Define colors based on 'Finished' column
colors = ['blue' if finish else 'red' for finish in finished]

# Plotting
plt.scatter(x, y, c=colors, alpha=0.5)

# Adding labels and title
plt.xlabel('Total Distance')
plt.ylabel('Times Charged')
plt.title(
    f'Scatter Plot of Total Distance vs Times Charged (Battery Threshold: {threshold}, Num Stations: {num_stations})')

# Adding legend
plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Finished'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Not Finished')])

# Showing plot
plt.show()

# Boxplot for Total Distance
plt.figure(figsize=(8, 6))
plt.boxplot(df['Total Distance'], patch_artist=True)
plt.title('Boxplot of Total Distance')
plt.ylabel('Total Distance')
plt.show()



# Calculate mean total distance for each combination of battery threshold and number of stations
mean_distance = results_all_df.groupby(['Battery Threshold', 'Num Stations'])['Total Distance'].mean().reset_index()

# Calculate mean times charged for each combination of battery threshold and number of stations
mean_times_charged = results_all_df.groupby(['Battery Threshold', 'Num Stations'])['Times Charged'].mean().reset_index()

# Calculate percentage of finished simulations for each combination of battery threshold and number of stations
percentage_finished = results_all_df.groupby(['Battery Threshold', 'Num Stations'])['Finished'].mean().reset_index()
percentage_finished['Finished'] *= 100  # Convert to percentage

# Print the results
print("Mean Total Distance:")
print(mean_distance)
print("\nMean Times Charged:")
print(mean_times_charged)
print("\nPercentage Finished:")
print(percentage_finished)

# Visualize the results
plt.figure(figsize=(15, 5))

# Mean Total Distance
plt.subplot(1, 3, 1)
for threshold in battery_thresholds:
    plt.plot(mean_distance[mean_distance['Battery Threshold'] == threshold]['Num Stations'],
             mean_distance[mean_distance['Battery Threshold'] == threshold]['Total Distance'], label=f"Threshold: {threshold}")
plt.xlabel('Number of Stations')
plt.ylabel('Mean Total Distance')
plt.title('Mean Total Distance vs Number of Stations')
plt.legend()

# Mean Times Charged
plt.subplot(1, 3, 2)
for threshold in battery_thresholds:
    plt.plot(mean_times_charged[mean_times_charged['Battery Threshold'] == threshold]['Num Stations'],
             mean_times_charged[mean_times_charged['Battery Threshold'] == threshold]['Times Charged'], label=f"Threshold: {threshold}")
plt.xlabel('Number of Stations')
plt.ylabel('Mean Times Charged')
plt.title('Mean Times Charged vs Number of Stations')
plt.legend()

# Percentage Finished
plt.subplot(1, 3, 3)
for threshold in battery_thresholds:
    plt.plot(percentage_finished[percentage_finished['Battery Threshold'] == threshold]['Num Stations'],
             percentage_finished[percentage_finished['Battery Threshold'] == threshold]['Finished'], label=f"Threshold: {threshold}")
plt.xlabel('Number of Stations')
plt.ylabel('Percentage Finished (%)')
plt.title('Percentage Finished vs Number of Stations')
plt.legend()

plt.tight_layout()
plt.show()

