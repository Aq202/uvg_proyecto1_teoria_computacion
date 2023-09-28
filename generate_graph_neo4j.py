from py2neo import Graph, Node, Relationship


def generate_graph_neo4j(AFD):
    graph = Graph("bolt://localhost:7687")

    #limpiar bd
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    graph.run(query)

    nodes_graph = {}

    nodes = {state: f'{{q{i}}}' for i, state in enumerate([tuple(st) for st in AFD['STATES']])}
    acceptance_nodes = [value for (key, value) in nodes.items() if key in AFD['ACCEPTANCE']]

    def add_node(node_id, type="STATE"):
        node_type = "ACCEPTANCE" if node_id in acceptance_nodes else type
        node = Node(node_type, nombre=node_id)
        nodes_graph[node_id] = node
        graph.create(node)
        return node
    
    def add_relationship(node1, relation, node2):
        rel = Relationship(node1, relation, node2)
        graph.create(rel)

    start_node = nodes[tuple(AFD['INITIAL_STATE'])]
    begin = 'start'
    n1 = add_node(begin, 'START')
    n2 = add_node(start_node)
    add_relationship(n1, ' ', n2)
    edge_labels = dict()

    print('DICCIONARIO DE ESTADOS:')
    for (key, value) in nodes.items():
        print(f'State: {key}, Alias: {value}')

    for transition in AFD['TRANSITIONS']:
        node1 = tuple(transition[0])
        node2 = tuple(transition[2])
        label = transition[1]
        if nodes[node1] not in nodes_graph:
            add_node(nodes[node1])
        if nodes[node2] not in nodes_graph:
            add_node(nodes[node2])
        
        add_relationship(nodes_graph[nodes[node1]], label, nodes_graph[nodes[node2]])
        if (nodes[node1], nodes[node2]) in edge_labels.keys():
            edge_labels[(nodes[node1], nodes[node2])] = f'{edge_labels[(nodes[node1], nodes[node2])]}, {label}'
        else:
            edge_labels[(nodes[node1], nodes[node2])] = label


