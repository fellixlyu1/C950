# Created by Dong Seong Lyu
# Student ID: 011326964
import package
import csv
import datetime
import truck
from hashmap import HashMap

# Sets a hash table for the packages.csv data
package_table = HashMap()


# Extracts package information into a Hash Table by inserting the assorted package ID and its corresponding information.
# The time complexity of set_package_hashmap is O(n)
def set_package_hashmap(hash_table):
    with open("csv_files/packages.csv") as packages_csv:
        packages_data = list(csv.reader(packages_csv, delimiter=","))
        for phk in packages_data:
            package_hash_keys = package.Package(int(phk[0]), phk[1], phk[2], phk[3],
                                                phk[4], phk[5], phk[6], phk[7])
            hash_table.insert(int(phk[0]), package_hash_keys)


# Extracts addresses from the addresses.csv data and converts them into address ID. The time complexity of
# set_address_id is O(n).
def set_address_id(address):
    with open("csv_files/addresses.csv") as addresses_csv:
        addresses_data = list(csv.reader(addresses_csv, delimiter=","))
        for a in addresses_data:
            if address == a[2]:
                address_id = int(a[0])
                return address_id


# Extracts the data from the distances.csv file. The time complexity of the set_distance_mileage method is O(n^2).
def set_distance_mileage(distances_file):
    with open(distances_file) as distances_csv:
        distances_data = list(csv.reader(distances_csv, delimiter=","))
        for i in range(len(distances_data)):
            for j in range(len(distances_data)):
                if i < j:
                    distances_data[i][j] = distances_data[j][i]
        return distances_data


distances_table = set_distance_mileage("csv_files/distances.csv")


# Gets the package id numbers and calls the address data of that id from the Chaining Hash Table. The time complexity of
# the get_package_address is O(n).
def get_package_address(package_id):
    package_address = []
    set_package_hashmap(package_table)
    package_address.append(package_table.lookup(package_id))
    for i in package_address:
        return i.address


# Using the address data, this method calculates the distance between the package and the Hub. The time complexity is
# O(n).
def get_distance_from_hub(package_id):
    x = get_package_address(package_id)
    y = set_address_id(x)
    return distances_table[0][y]


# Using the address data, the get_distances_between_locations method calculates the distance miles from
# two locations. The time complexity of get_distances_between_locations is O(n).
def get_distances_between_locations(loc1, loc2):
    x = set_address_id(get_package_address(loc1))
    y = set_address_id(get_package_address(loc2))
    return distances_table[x][y]


# The get_nearest_package_from_hub method uses the truckload and uses the elements in the truckload list to compare
# individual elements in the list of packages to call back which package is going to be the nearest from the hub.
# The time complexity of the get_nearest_package_from_hub method is O(n).
def get_nearest_package_from_hub(package_load):
    nearest_package = None
    nearest_distance = float('inf')

    for i in package_load:
        distance = float(get_distance_from_hub(i))
        if distance != 0.0 and distance < nearest_distance:
            nearest_distance = distance
            nearest_package = i

    return nearest_package


# By using a special floating-point value, it indicates an unbounded upper limit that is used to compare the
# distances between the package order inputted and the rest of the elements in the list. This method goes from the first
# package in the list, scanning the next package in the list and calls back the package that is closest to the
# package_order. The time complexity of the get_nearest_package is O(n).

def get_nearest_package(package_order, package_load):
    nearest_package = None
    nearest_distance = float('inf')

    for i in package_load:
        distance = float(get_distances_between_locations(package_order, i))
        if distance != 0.0 and distance < nearest_distance:
            nearest_distance = distance
            nearest_package = i

    return nearest_package


# Using the nearest neighbor algorithm, I created a method to re-sort the load of packages in trucks 1 to 3 according
# to the most optimal routes and shortest distances between all the packages. First, the nearest_neighbor method
# takes the truck's packages and assigns unvisited_packages as a copy of the list of package ids. The route is an empty
# list. The time complexity of the nearest_neighbor is O(n).
def nearest_neighbor(package_load):
    unvisited_packages = package_load.copy()
    route = []
    packages_from_hub = get_nearest_package_from_hub(package_load)
    hub_to_next_package = get_nearest_package(packages_from_hub, unvisited_packages)
    route.append(packages_from_hub)
    i = get_nearest_package(hub_to_next_package, unvisited_packages)
    unvisited_packages.remove(packages_from_hub)

    while unvisited_packages:
        nearest_package = get_nearest_package(i, unvisited_packages)
        i = nearest_package
        route.append(nearest_package)
        unvisited_packages.remove(nearest_package)

    return route


truckload1 = [1, 13, 14, 15, 16, 19, 20, 26, 29, 30, 31, 34, 37, 40]
truckload2 = [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 17, 25, 36]
truckload3 = [9, 18, 21, 22, 23, 24, 27, 28, 32, 33, 35, 38, 39]

t_time1 = datetime.timedelta(hours=8, minutes=0, seconds=0)
t_time2 = datetime.timedelta(hours=9, minutes=5, seconds=0)
t_time3 = datetime.timedelta(hours=10, minutes=20, seconds=0)


# The get_all_package_distances method sorts the list from the trucks using the nearest_neighbor method, then uses the
# get_distance_from_hub method to find the distance from the first package from the hub. Once the first package is
# delivered, the get_distance_between method find the distances from the next package on the list to the one after
# and loops through the list until all packages have been delivered. The get_all_package_distances method has a time
# complexity of O(n).
def get_all_package_distances(truckload):
    sorted_route = nearest_neighbor(truckload)
    all_package_dist = []
    first_truck_dist = float(get_distance_from_hub(sorted_route[0]))
    all_package_dist.append(first_truck_dist)

    for i in range(len(sorted_route) - 1):
        dist_between_packages = float(get_distances_between_locations(sorted_route[i], sorted_route[i + 1]))
        all_package_dist.append(dist_between_packages)

    return all_package_dist


# Using a simple sum function, I created a method to display the total distance of the truckload in the truck. The
# time complexity of the get_total_distance method is O(n).
def get_total_distance(truckload):
    ind_package_dist = get_all_package_distances(truckload)
    td = float(sum(ind_package_dist))
    return td


# The distance_time_conversion method converts the distances between the packages and converts the distances into
# seconds re-formats the seconds to show the progressed clock time. The get_all_package_distances method will take the
# packages from the truckload as the input and uses a for loop to read scan each of the elements in the list, which
# will result in the sorted routes. The time complexity of the distance_time_conversion is O(n).
def distance_time_conversion(truckload, truck_time):
    sorted_distances = get_all_package_distances(truckload)
    times = []
    for t in range(len(sorted_distances)):
        amount_of_seconds = datetime.timedelta(seconds=sorted_distances[t] / (18 / 3600))
        truck_time = truck_time + amount_of_seconds
        hours = truck_time.total_seconds() // 3600
        minutes = (truck_time.total_seconds() // 60) % 60
        seconds = truck_time.total_seconds() % 60
        formatted_time = f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
        times.append(formatted_time)

    return times


# The update_wrong_info method is a recursive method that is being used with the distance_time_conversion method to
# search if the relative information from the updated package data matches with the Package ID: 9 and removes the info
# to insert the new item which changes the information into the updated information after 10:20:00 AM. The
# update_wrong_info method has a time complexity of O(n).
def update_wrong_info(hash_table, truckload):
    set_package_hashmap(hash_table)
    check_if = hash_table.lookup(9)
    if check_if == truckload:
        hash_table.remove(9)
        hash_table.insert(9, "9,410 S. State St.,Salt Lake City,UT,84111,,,,,,,,")


update_wrong_info(package_table, truckload3)


# The get_time_lists method is used to find the best sorted routes according to the package ID. This method is going to
# be used for one other method. It initializes the nearest_neighbor of each of the truckloads and assigned 'first',
# 'second', and 'third', then uses the package ID and finds it in the list that is called from nearest_neighbor.
# The time complexity of this method is O(n).
def get_time_lists(p_id):
    first = nearest_neighbor(truckload1)
    second = nearest_neighbor(truckload2)
    third = nearest_neighbor(truckload3)
    if p_id in first:
        i = int(first.index(p_id))
        t_list1 = distance_time_conversion(truckload1, t_time1)
        return t_list1[i]
    elif p_id in second:
        i = int(second.index(p_id))
        t_list2 = distance_time_conversion(truckload2, t_time2)
        return t_list2[i]
    elif p_id in third:
        i = int(third.index(p_id))
        t_list3 = distance_time_conversion(truckload3, t_time3)
        return t_list3[i]


# The delivery_status method sets up the package hashmap to use the lookup function in the order. Taking the time of
# each package ID, the delivery_status method then makes comparisons with the inputted time to see if the package
# is either "EN ROUTE" or "DELIVERED". Once this is initialized, the method will call the information from the hashmap,
# the time of the package, and the status. The time complexity of the delivery_status method is O(n).
def delivery_status(p_id, inputted_time):
    set_package_hashmap(package_table)
    tl = get_time_lists(p_id)
    for i in range(len(tl)):
        if inputted_time < tl:
            status = "EN ROUTE"
            printed_truck = truck.Truck(str(package_table.lookup(p_id)), tl, status)
            return printed_truck
        elif inputted_time >= tl:
            status = "DELIVERED"
            printed_truck = truck.Truck(str(package_table.lookup(p_id)), tl, status)
            return printed_truck


# The get_truck_time_lists method takes a truckload's packages as a list and checks which truckload it is and calls the
# times of each package being sorted and delivered through the nearest neighbor algorithm. The time complexity of
# this method will be O(n).
def get_truck_time_lists(truckload):
    if truckload == truckload1:
        t_list1 = distance_time_conversion(truckload1, t_time1)
        return t_list1
    elif truckload == truckload2:
        t_list2 = distance_time_conversion(truckload2, t_time2)
        return t_list2
    elif truckload == truckload3:
        t_list3 = distance_time_conversion(truckload3, t_time3)
        return t_list3


# The delivery_status_of_all method takes the truckload, from_time, and to_time as arguments in the parameter. Each of
# the arguments is used to output the necessary information of each package and checking whether the packages have
# been delivered or en-route according to the user's inquiries about each package's delivery status, address, city,
# state, zip code, weight, notes, delivery time, and status. The time complexity of delivery_status_of_all will be
# O(n).
def delivery_status_of_all(truckload, from_time, to_time):
    nn = nearest_neighbor(truckload)
    tl = get_truck_time_lists(truckload)
    for i in range(len(nn)):
        time = tl[i]
        pos = nn[i]
        if from_time <= time <= to_time:
            print(delivery_status(p_id=pos, inputted_time=to_time))
            i += 1
        elif from_time > time:
            print(delivery_status(p_id=pos, inputted_time=to_time))
            i += 1
        elif to_time < time:
            print(delivery_status(p_id=pos, inputted_time=to_time))
            i += 1
        else:
            break


class Main:
    header = "___________________________________________"
    welcome_mess = "Welcome to the Western Governors University"
    footer = "___________________________________________"
    print(header)
    print(welcome_mess)
    print(footer + "\n")
    print("Truck 1")
    print("Best Route: ", nearest_neighbor(truckload1))
    print("Schedule of each package: ", get_truck_time_lists(truckload1))
    print("Total distance from Truck 1: ", get_all_package_distances(truckload1), "\n")
    print("Truck 2")
    print("Best Route: ", nearest_neighbor(truckload2))
    print("Schedule of each package: ", get_truck_time_lists(truckload2))
    print("Total distance from Truck 2: ", get_all_package_distances(truckload2), "\n")
    print("Truck 3")
    print("Best Route: ", nearest_neighbor(truckload3))
    print("Schedule of each package: ", get_truck_time_lists(truckload3))
    print("Total distance from Truck 3: ", get_all_package_distances(truckload3), "\n")
    print("\n")
    print("Total Distance of Each Truck")
    print("Total Distance of Truck 1: " + str(get_total_distance(truckload1)))
    print("Total Distance of Truck 2: " + str(get_total_distance(truckload2)))
    print("Total Distance of Truck 3: " + str(get_total_distance(truckload3)) + "\n")
    print("Total miles traveled: ")
    print(str(round(get_total_distance(truckload1) + get_total_distance(truckload2) + get_total_distance(truckload3)))
          + "\n")
    print("Delivery Statuses of all packages in Truck 1 (Pick times to check which packages were delivered or"
          " en route):")
    delivery_status_of_all(truckload1, input("Pick a time to choose from (format: HH:MM:SS): "),
                           input("Pick a time to choose to (format: HH:MM:SS): "))
    print("\n")
    print("Delivery Statuses of all packages in Truck 2 (Pick times to check which packages were delivered or"
          " en route):")
    delivery_status_of_all(truckload2, input("Pick a time to choose from (format: HH:MM:SS): "),
                           input("Pick a time to choose to (format: HH:MM:SS): "))
    print("\n")
    print("Delivery Statuses of all packages in Truck 3 (Pick times to check which packages were delivered or"
          " en route):")
    delivery_status_of_all(truckload3, input("Pick a time to choose from (format: HH:MM:SS): "),
                           input("Pick a time to choose to (format: HH:MM:SS): "))
