import json


# подсчет показателя связанности графа graph без вершины absent_node
def graph_connect(graph, clients_by_nodes, absent_node):
    new_graph = graph_remove(graph, absent_node)
    visited = dict((_, 0) for _ in new_graph)
    connect_val = 0                             # показатель связности всего графа без данной вершины

    for node in new_graph:
        if visited[node]:
            continue

        visited[node] = 1
        cur_val = clients_by_nodes[node]        # показатель связности конкретного компонента связности

        stack = [node]
        while stack:
            cur = stack.pop()
            for to in new_graph[cur]:
                if not visited[to]:
                    visited[to] = 1
                    stack.append(to)
                    cur_val += clients_by_nodes[to]

        connect_val += cur_val ** 2

    connect_val += clients_by_nodes[absent_node]

    return connect_val


# создаем подграф new_graph графа graph без вершины node
def graph_remove(graph, node):
    new_graph = {key: val for (key, val) in graph.items() if key != node}
    for v in new_graph:
        new_graph[v] = [_ for _ in new_graph[v] if _ != node]
    return new_graph


# создаем словарь смежноти графа по списку ребер node_connections
# и списку вершин nodes
def create_graph(nodes, node_connections):
    graph = dict((_, []) for _ in nodes)

    for m in node_connections:
        if not m[1] in graph[m[0]]:
            graph[m[0]].append(m[1])

        if not m[0] in graph[m[1]]:
            graph[m[1]].append(m[0])

    return graph


# поиск наиболее важных вершин графа
def find_main_node(json_string):
    node_connections, clients_by_nodes = json.loads(json_string)
    graph = create_graph(clients_by_nodes.keys(), node_connections)
    importance = {_: 0 for _ in graph}

    for node in graph:
        connect_val = graph_connect(graph, clients_by_nodes, node)
        importance[node] = connect_val

    min_val = min(importance.values())
    most_important = [node for node in graph if importance[node] == min_val]
    return most_important

