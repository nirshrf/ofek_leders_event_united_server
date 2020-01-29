JSON_dictionary = dict(Quadcopter='{id, name, launchtime, isfree, x, y}',
                       PetType='{code, description}',
                       EventStatus='{code, description}',
                       Coordinate='{longitude, latitude}',
                       AdoptionStatus='{code, description}',
                       History='{id, petType{code, description}, amount}',
                       GridCell='{x, y, lastPictureUrl, petType{code, description}}',
                       Adopter='{id, preferred{code, description}, secondpreferred{code, description}, isvalid}',
                       Event='{quadcopter{id, name, launchtime, isfree, x, y}, gridCell{id, x, y, lastPictureUrl, history{id, petType{code, description}, amount}}, eventTime, eventStatus{code, description}}',
                       Adoptee='{petType{code, description}, x, y, imageBeforeURL, imageAfterURL, adoptionStatus{code, description}}',
                       AiStatus='{toggleDroneAI, togglePetsAI, toggleAdoptionAI, toggleBdaAI}',
                       Plot='{timestamp, x, y, z}',
                       GridCell_plots='{x, y, plot{timestamp, x, y, z}}')


def get_entity_as_json(entity):
    if entity in JSON_dictionary.keys():
        return JSON_dictionary[entity]
    raise KeyError
