from django.shortcuts import render
import heapq
from django.http import HttpResponse
import json
# Create your views here.

def say_Hello():
    return HttpResponse('Hello world!')

def home(request):
    print('requested')
    if(request.method == 'POST'):
        puzzel = request.POST["puzzel"]
        print(puzzel)
        puzzel = json.loads(puzzel)
        
        # print('xxxxxxxxxxxxxxxxxxxxxx')
        puzzel=[int(num) if num.isdigit() else 0 for num in puzzel]
        print(puzzel)
        # print('yyyyyyyyyyyyyyyyyy')
        puzzel = tuple(puzzel)
        # print(puzzel)
        solution=  solve_puzzle(puzzel)
        print(solution)
        return HttpResponse(json.dumps(solution))
    print('get')
    return render(request,'home.html')




class PuzzleState:
    def __init__(self, board, moves=0, previous=None):
        self.board = board
        self.moves = moves
        self.previous = previous
        self.blank = board.index(0)

    def __lt__(self, other):
        return self.priority() < other.priority()

    def priority(self):
        return self.moves + self.manhattan_distance()

    def manhattan_distance(self):
        distance = 0
        for i in range(9):
            if self.board[i] != 0:
                x, y = divmod(i, 3)
                goal_x, goal_y = divmod(self.board[i] - 1, 3)
                distance += abs(x - goal_x) + abs(y - goal_y)
        return distance

    def neighbors(self):
        def swap_positions(board, pos1, pos2):
            board = list(board)
            board[pos1], board[pos2] = board[pos2], board[pos1]
            return tuple(board)

        neighbors = []
        x, y = divmod(self.blank, 3)
        if x > 0:
            neighbors.append(PuzzleState(swap_positions(self.board, self.blank, self.blank - 3), self.moves + 1, self))
        if x < 2:
            neighbors.append(PuzzleState(swap_positions(self.board, self.blank, self.blank + 3), self.moves + 1, self))
        if y > 0:
            neighbors.append(PuzzleState(swap_positions(self.board, self.blank, self.blank - 1), self.moves + 1, self))
        if y < 2:
            neighbors.append(PuzzleState(swap_positions(self.board, self.blank, self.blank + 1), self.moves + 1, self))
        return neighbors

    def is_goal(self):
        return self.board == (1, 2, 3, 4, 5, 6, 7, 8, 0)


def solve_puzzle(start_board):
    start_state = PuzzleState(start_board)
    open_list = []
    heapq.heappush(open_list, start_state)
    closed_set = set()

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state.board)
                current_state = current_state.previous
            return path[::-1]  # Reverse the path to get from start to goal

        closed_set.add(current_state.board)

        for neighbor in current_state.neighbors():
            if neighbor.board not in closed_set:
                heapq.heappush(open_list, neighbor)

    return None
