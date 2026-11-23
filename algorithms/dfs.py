from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        """Busca em profundidade com limite de profundidade (pilha LIFO).

        Mantém a menor profundidade em que cada estado foi alcançado, para não
        reexpandir um estado por um caminho igual ou mais longo (evita ciclos).
        """
        nodes_expanded = 0
        nodes_generated = 1
        frontier = [initial]
        best_depth = {initial.tiles: 0}
        max_frontier_size = 1

        while frontier:
            node = frontier.pop()

            # O nó pode ter sido alcançado depois por um caminho mais curto
            if best_depth.get(node.tiles, node.cost) < node.cost:
                continue

            if node.is_goal:
                return SearchResult(node, nodes_expanded, nodes_generated,
                                    max_frontier_size, node.cost)

            if node.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            # Empilha em ordem inversa para explorar na ordem UP, DOWN, LEFT, RIGHT
            for child in reversed(node.neighbors()):
                nodes_generated += 1
                previous = best_depth.get(child.tiles)
                if previous is not None and previous <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
