from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1  # o estado inicial

        if initial.is_goal:
            return SearchResult(initial, nodes_expanded, nodes_generated, 1, initial.cost)

        frontier = deque([initial])
        reached = {initial.tiles}  # estados já gerados (na fronteira ou explorados)
        max_frontier_size = 1

        while frontier:
            node = frontier.popleft()
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.tiles in reached:
                    continue
                # Teste de objetivo na geração (BFS continua ótima com custo unitário)
                if child.is_goal:
                    return SearchResult(child, nodes_expanded, nodes_generated,
                                        max_frontier_size, child.cost)
                reached.add(child.tiles)
                frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
