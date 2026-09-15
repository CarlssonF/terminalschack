import sys

# test att göra funktion istället för att alltid skriva ut i print vilken färg
def pr_red(message): print("\033[91;1m {}\033[00m" .format(message))


def create_board():
    return [["T", "H", "L", "D", "K", "L", "H", "T"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["b", "b", "b", "b", "b", "b", "b", "b"],
            ["t", "h", "l", "d", "k", "l", "h", "t"]]


def print_board(board):
    print("\033[93;1m  a b c d e f g h\033[00m")
    row_number = 8
    for row in board:
        print("\033[93;1m {}\033[00m" .format(row_number), end =" ")
        print(*row, sep="|")
        row_number -= 1


def create_board_dict(board):
    board_dict = {}
    for row_index, row in enumerate(board):
        for col_index, piece in enumerate(row):
            if piece != " ":
                position = (row_index, col_index)
                color = "Svart" if piece.isupper() else "Vit"
                board_dict[position] = (piece, color)
    return board_dict

def print_valid_moves(board_dict, current_pos, board, call_function = True):
    moves = []
    piece, color = board_dict[current_pos]
    if piece.casefold() == "b":
        moves = valid_pawn_moves(*current_pos, color, board_dict)
    elif piece.casefold() == "t":
        moves = valid_rook_moves(*current_pos, board, board_dict) 
    elif piece.casefold() == "h":
        moves = valid_knight_moves(*current_pos, board_dict) 
    elif piece.casefold() == "l":
        moves = valid_bishop_moves(*current_pos, board, board_dict) 
    elif piece.casefold() == "k":
        moves = valid_king_moves(*current_pos, board_dict) 
    elif piece.casefold() == "d":
        moves = valid_queen_moves(*current_pos, board, board_dict)
    
    valid_moves= []
    for move in moves:
        sim_board_dict = board_dict.copy() #"simulerat" bräde för att se om drag leder till schack
        sim_board_dict[current_pos] = (' ', color)
        sim_board_dict[move] = (piece, color)
        if not call_function or not is_checked(sim_board_dict, board, color): #om den antingen inte anropas från is_check eller draget inte är i schack
            valid_moves.append(move)

    return valid_moves


def get_current_pos():
    while True:
        try:
            value = input("Skriv in nuvarande koordinater för pjäsen du vill flytta (tex a2): ")
            if value.lower == "stopp":
                sys.exit(0)
            column, row = value[0], value[1]
            column_index = ord(column.lower) - ord('a')
            row_index = 8 - int(row)
            if 0 <= row_index < 8 and 0 <= column_index < 8:
                return int(row_index), int(column_index)
        except (ValueError, IndexError):
            pr_red("Ogiltig koordinat, testa igen:")


def get_dest_pos():
    while True:
        try:
            value = input("Skriv in koordinater för rutan du vill flytta till (tex a2): ")
            if value == "Stopp":
                sys.exit(0)
            column, row = value[0], value[1]
            column_index = ord(column.lower()) - ord('a') 
            row_index = 8 - int(row)
            if 0 <= row_index < 8 and 0 <= column_index < 8:
                return int(row_index), int(column_index)
        except (ValueError, IndexError):
            pr_red("Ogiltig koordinat, testa igen:")

#definitioner av alla grunddrag + funktioner för att lista alla giltiga drag för olika pjäser

def pawn_move(current_row, current_col, dest_row, dest_col, color):
    direction = -1 if color == "Vit" else 1
    return current_col == dest_col and (current_row + direction) == dest_row


def valid_pawn_moves(current_row, current_col, color, board_dict):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if pawn_move(current_row, current_col, row, col, color) and can_capture_piece(current_row, current_col, row, col, board_dict):
                valid_moves.append((row, col))
    return valid_moves


def bishop_move(current_row, current_col, dest_row, dest_col, board):
    if abs(dest_col - current_col) == abs(dest_row - current_row):
        row_step = 1 if dest_row > current_row else -1
        col_step = 1 if dest_col > current_col else -1
        current_check_pos = (current_row + row_step, current_col + col_step)
        while current_check_pos != (dest_row, dest_col):
            if board[current_check_pos[0]][current_check_pos[1]] != " ":
                return False  # det står en pjäs ivägen
            current_check_pos = (current_check_pos[0] + row_step, current_check_pos[1] + col_step)
        return True
    return False 


def valid_bishop_moves(current_row, current_col, board, board_dict):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if bishop_move(current_row, current_col, row, col, board) and can_capture_piece(current_row, current_col, row, col, board_dict):
                valid_moves.append((row, col))
    return valid_moves


def rook_move(current_row, current_col, dest_row, dest_col, board):
    if current_col == dest_col or current_row == dest_row:
        if current_row == dest_row: # pjäsen rör sig horisiontellt
            step = 1 if current_col < dest_col else -1
            for col in range(current_col + step, dest_col, step):
                if board[current_row][col] != " ":
                    return False
        else: # pjäsen rör sig vertikalt
            step = 1 if current_row < dest_row else -1
            for row in range(current_row + step, dest_row, step):
                if board[row][current_col] != " ":
                    return False
        return True


def valid_rook_moves(current_row, current_col, board, board_dict):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if rook_move(current_row, current_col, row, col, board) and can_capture_piece(current_row, current_col, row, col, board_dict):
                valid_moves.append((row, col))
    return valid_moves

def knight_move(current_row, current_col, dest_row, dest_col):
    row_diff = abs(dest_row - current_row)
    col_diff = abs(dest_col - current_col)
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)


def valid_knight_moves(current_row, current_col, board_dict):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if knight_move(current_row, current_col, row, col) and can_capture_piece(current_row, current_col, row, col, board_dict):
                valid_moves.append((row, col))
    return valid_moves


def queen_move(current_row, current_col, dest_row, dest_col, board):
    return bishop_move(current_row, current_col, dest_row, dest_col, board) or rook_move(current_row, current_col, dest_row, dest_col, board)


def valid_queen_moves(current_row, current_col, board, board_dict):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if queen_move(current_row, current_col, row, col, board) and can_capture_piece(current_row, current_col, row, col, board_dict):
                valid_moves.append((row, col))
    return valid_moves


def king_move(current_row, current_col, dest_row, dest_col):
    row_diff = abs(dest_row - current_row)
    col_diff = abs(dest_col - current_col)
    return row_diff == 1 or col_diff == 1


def valid_king_moves(current_row, current_col, board_dict):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if king_move(current_row, current_col, row, col) and can_capture_piece(current_row, current_col, row, col, board_dict):
                valid_moves.append((row, col))
    return valid_moves

# se om pjäsen på destinationsrutan "går att ta" (är av motståndarfärg eller är tom) 
def can_capture_piece(current_row, current_col, dest_row, dest_col, board_dict):
    if (dest_row, dest_col) in board_dict:
        current_color = board_dict[(current_row, current_col)][1]
        dest_color = board_dict[(dest_row, dest_col)][1]
        return current_color != dest_color
    else:
        return True

# identifiera om kungen är i schack
def is_checked(board_dict, board, current_player_color):
    king_pos = None
    for pos, (piece, color) in board_dict.items():
        if piece.lower() == 'k' and color == current_player_color:
            king_pos = pos
            break
    if king_pos == None:
        return False
    opponent_color = "Svart" if current_player_color == "Vit" else "Vit"
    for pos, (piece, color) in board_dict.items():
        if color == opponent_color:
            valid_moves = print_valid_moves(board_dict, pos, board, call_function = False) #undviker att funktionerna anropar varandra oändligt
            if king_pos in valid_moves:
                return True


#om true i kombo med is_checked är true är det matt, annars patt om det inte finns giltiga drag men inte är schack 
def is_checkmate(board_dict, board, current_player_color):
    for pos, (piece, color) in board_dict.items():
        if color == current_player_color:
            valid_moves = print_valid_moves(board_dict, pos, board)
            for move in valid_moves:
                sim_board_dict = board_dict.copy()
                sim_board_dict[pos] = (' ', color)
                sim_board_dict[move] = (piece, color)
                if not is_checked(sim_board_dict, board, color): #om det finns ett möjligt drag som förhindrar schack är det inte matt
                    return False
    return True

def game_status(board_dict, board, current_player_color):
    if is_checked(board_dict, board, current_player_color):
        if is_checkmate(board_dict, board, current_player_color):
            print("\033[31;1mSCHACK!!\033[0m\n")
            return True
        else:
            print("\033[31;1mSCHACKMATT!!\033[0m\n")
            return False
    elif is_checkmate(board_dict, board, current_player_color):
        print("\033[31;1mPATT!!\033[0m\n")
        return False
    else:
        return True

# lägg till tagna pjäser i listor
def capture_piece(current_row, current_col, dest_row, dest_col, board_dict, captured_white_pieces, captured_black_pieces):
    if can_capture_piece(current_row, current_col, dest_row, dest_col, board_dict) and (dest_row, dest_col) in board_dict:
        current_color = board_dict[(current_row, current_col)][1]
        if current_color == "Vit":
            captured_black_pieces.append(board_dict[(dest_row, dest_col)][0])
        else:
            captured_white_pieces.append(board_dict[(dest_row, dest_col)][0])
    return captured_white_pieces, captured_black_pieces

    
# returnera nytt bräde efter förflyttning
def new_board(source_board, current_row, current_col, dest_row, dest_col):
    board = [row[:] for row in source_board]
    piece_to_move = board[current_row][current_col]
    board[current_row][current_col] = " "
    board[dest_row][dest_col] = piece_to_move
    return board


def main():
    captured_white_pieces = []
    captured_black_pieces = []

    # printa schackbrädet i startposition
    current_player_color = "Vit"
    board = create_board()
    board_dict = create_board_dict(board)
    print("\nDu kan alltid avsluta genom att skriva \033[31;1mStopp\033[0m\n")
    print_board(board)

    # skriv vilken pjäs som står på rutan
    current_pos = None
    while True:

        if game_status(board_dict, board, current_player_color): #spelet fortsätter inte om matt eller patt

            print(f"\nDet är \033[92;1m {current_player_color}s \033[0m tur att flytta.")
            
            current_pos = get_current_pos() # input av position för pjäs att flytta och lista giltiga drag

            if current_pos in board_dict and board_dict[current_pos][1] == current_player_color:
                if current_pos in board_dict:
                    piece, color = board_dict[current_pos]
                    valid_moves = print_valid_moves(board_dict, current_pos, board)
                    if len(valid_moves) == 0:
                        print("Pjäsen har inga giltiga drag, testa att flytta en annan")
                    else:
                        print(f"På {current_pos} står det en {color} {piece} och giltiga drag är: ")
                        for move in valid_moves:
                            print(move)
                        
                        # input av destination och flytta pjäs
                        while True:
                            dest_pos = get_dest_pos()
                            if dest_pos in print_valid_moves(board_dict, current_pos, board):
                                captured_white_pieces, captured_black_pieces = capture_piece(*current_pos,*dest_pos, board_dict, captured_white_pieces, captured_black_pieces)
                                board = new_board(board, *current_pos, *dest_pos)
                                print_board(board) #printa nytt bräde
                                board_dict = create_board_dict(board)
                                print(f"Tagna vita pjäser: {captured_white_pieces} \nTagna svarta pjäser: {captured_black_pieces}")
                                current_player_color = "Svart" if current_player_color == "Vit" else "Vit"
                                break
                            else:
                                print("Draget är inte giltigt, testa igen")
                else:
                    print(f"Det står ingen pjäs på {current_pos}")
            else:
                print(f"Det står ingen pjäs av din färg på {current_pos}")
        else:
            break

# bra prectice så att programmet inte automatiskt körs om någon annan hämtar det, om det inte är från main
if __name__ == "__main__":
    main()