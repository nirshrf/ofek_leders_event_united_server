from model import generate_model
from confusion_matrix import compute_confusion_matrix
from generations.generateHeatmap import generate_heat_map

model = generate_model()
confusion_matrix = compute_confusion_matrix(model)
JAVA_server_url = 'https://adoptionserver-1580505813958.azurewebsites.net/graphql'
grid_distribution = generate_heat_map()
thread_flags = dict(drones_executor_flag=False,
                    classifier_flag=False,
                    match_maker_flag=False)
