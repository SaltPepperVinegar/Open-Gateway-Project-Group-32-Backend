from .number_verification import number_verification
from .population_density_data import population_density_data
from .region_device_count import region_device_count

print("\n==============number verification============== \n")
number_verification()

print("\n==============population density data============== \n")
population_density_data()

print("\n==============regional device count============== \n")
region_device_count()

while True:
    input("continue: ")
    print("\n==============number verification============== \n")
    number_verification()

    print("\n==============population density data============== \n")
    population_density_data()

    print("\n==============regional device count============== \n")
    region_device_count()
