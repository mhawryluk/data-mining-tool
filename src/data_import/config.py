import psutil

PERCENT_TO_USE = 0.8
# available memory in bytes
AVAILABLE_RAM_MEMORY = int(psutil.virtual_memory().available * PERCENT_TO_USE)# / (1024**2)

# average size of element in data frame
SIZE_OF_VALUE = 8 * 20
