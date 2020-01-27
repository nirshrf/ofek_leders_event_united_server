import random as rd
from Entities import Quadcopter
from graphqlHandler import GraphQlMutation
from main import JAVA_server_url


def generate_quadcopters(amount):
    graph_handler = GraphQlMutation(JAVA_server_url)
    quads = [Quadcopter(q, "quad_"+q, 0, True, rd.randint(0, 99), rd.randint(0, 99)) for q in amount]
    graph_handler.set_quads(quads)
    print("generated quadcopters")

