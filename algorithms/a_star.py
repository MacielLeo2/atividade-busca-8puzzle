import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo
_GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça até sua posição
        no objetivo (o espaço vazio não conta). É admissível e consistente, pois
        cada movimento desloca uma única peça em exatamente uma casa."""
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = _GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1
        tie = count()  # desempate estável para a fila de prioridade

        # Entradas da fila: (f = g + h, h, ordem de inserção, estado)
        h0 = self.heuristic(initial)
        frontier = [(initial.cost + h0, h0, next(tie), initial)]
        best_cost = {initial.tiles: initial.cost}
        explored = set()
        max_frontier_size = 1

        while frontier:
            _, _, _, node = heapq.heappop(frontier)

            if node.tiles in explored:
                continue  # entrada obsoleta (já expandido por caminho melhor)

            if node.is_goal:
                return SearchResult(node, nodes_expanded, nodes_generated,
                                    max_frontier_size, node.cost)

            explored.add(node.tiles)
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.tiles in explored:
                    continue
                if child.cost < best_cost.get(child.tiles, float("inf")):
                    best_cost[child.tiles] = child.cost
                    h = self.heuristic(child)
                    heapq.heappush(frontier, (child.cost + h, h, next(tie), child))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
