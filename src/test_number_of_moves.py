from board import Board

def test_passed(FEN, correct_number):
    position = Board(FEN)
    position.update(print_info=False)
    position_nom = len(position.get_my_moves())
    result = position_nom == correct_number
    
    if result:
        print(f"Test passed.")
    else:
        print(f"Test failed.")
    
    return result
    

# Positions from chessprogramming.org (https://www.chessprogramming.org/Perft_Results#Perft_10)
positions = [
    ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", 48),
    ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 14),
    ("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", 6)
]

for i, position in enumerate(positions):
    passed = test_passed(*position)
