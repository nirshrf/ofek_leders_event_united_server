from model import generate_model
from confusion_matrix import compute_confusion_matrix
from generations.generateHeatmap import generate_heat_map

model = generate_model()
confusion_matrix = compute_confusion_matrix(model)
JAVA_server_url = 'http://cto.southcentralus.cloudapp.azure.com:9000/graphql'
grid_distribution = generate_heat_map()
