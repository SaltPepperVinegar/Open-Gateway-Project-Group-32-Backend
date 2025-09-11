from .api_token import get_token
from .auth_code import get_auth_code
from .config import * 
from .number_verification import number_verification
from .region_device_count import region_device_count
from .population_density_data import population_density_data


print("\n==============number verification============== \n")
number_verification()

print("\n==============population density data============== \n")
population_density_data()

print("\n==============regional device count============== \n")
region_device_count()
