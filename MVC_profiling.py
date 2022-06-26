import timeit
import random

from MVC import Model

def profiler(boards):
    model = Model()
    loop = 100
    loopai = 5
    result_random = []
    result_ai = []

    def create_random_board(taken_spots):
        currentPlayer = 1
        for i in range(taken_spots):
            availableSquare = model.findFreeSpot()
            if len(availableSquare) > 0:
                x = random.randint(0, len(availableSquare) - 1)
                row, column = model.findFreeSpot()[x]
                model.claimSpot(row, column, currentPlayer)
                currentPlayer = currentPlayer % 2 + 1
        return model.board

    for i in range(9):
        random_time = 0
        ai_time = 0
        for board in range(boards):
            model = Model()
            model.board = create_random_board(i)
            random_time += timeit.timeit(lambda: model.randomComputer(), number=loop)/loop
            ai_time += timeit.timeit(lambda: model.bestMove(), number=loopai)/loopai
            print(f"random : {random_time}")
            print(f"AI : {ai_time}")
        result_random.append(round(random_time/boards, 7))
        result_ai.append(round(ai_time/boards, 7))
    print(f"random : {result_random}")
    print(f"AI : {result_ai}")




if __name__ == '__main__':
    profiler(100)
