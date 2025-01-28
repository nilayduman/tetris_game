#bugün basit bir tetris oyunu yapacağım
import pygame
import random

pygame.init()

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    BLACK,
    (0, 240, 240),  # I - Cyan
    (240, 240, 0),  # O - Yellow
    (160, 0, 240),  # T - Purple
    (240, 160, 0),  # L - Orange
    (0, 0, 240),  # J - Blue
    (0, 240, 0),  # S - Green
    (240, 0, 0)  # Z - Red
]

# Oyun ayarları
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WIDTH = BLOCK_SIZE * BOARD_WIDTH
HEIGHT = BLOCK_SIZE * BOARD_HEIGHT
PANEL_WIDTH = 200
SCREEN_WIDTH = WIDTH + PANEL_WIDTH * 2

# Tetromino şekilleri ve renk indeksleri
SHAPES = [
    [[1, 1, 1, 1]],  # I (1)
    [[1, 1], [1, 1]],  # O (2)
    [[1, 1, 1], [0, 1, 0]],  # T (3)
    [[1, 1, 1], [1, 0, 0]],  # L (4)
    [[1, 1, 1], [0, 0, 1]],  # J (5)
    [[1, 1, 0], [0, 1, 1]],  # S (6)
    [[0, 1, 1], [1, 1, 0]]  # Z (7)
]


class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


class Game:
    def __init__(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_pieces = []
        self.hold_piece = None
        self.can_hold = True
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.bag = []
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.initialize_bag()
        self.spawn_new_piece()
        self.generate_next_pieces(5)

    def initialize_bag(self):
        self.bag = list(range(len(SHAPES)))
        random.shuffle(self.bag)

    def get_next_from_bag(self):
        if not self.bag:
            self.initialize_bag()
        return self.bag.pop()

    def spawn_new_piece(self):
        if not self.next_pieces:
            self.generate_next_pieces(5)
        shape_index = self.next_pieces.pop(0)
        self.current_piece = Tetromino(SHAPES[shape_index], shape_index + 1)
        self.generate_next_pieces(1)
        if self.check_collision():
            self.game_over = True

    def generate_next_pieces(self, count):
        while len(self.next_pieces) < count:
            if not self.bag:
                self.initialize_bag()
            self.next_pieces.append(self.get_next_from_bag())

    def check_collision(self, dx=0, dy=0):
        for y, row in enumerate(self.current_piece.shape):
            for x, val in enumerate(row):
                if val:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False

    def rotate_piece(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision():
            self.current_piece.shape = original_shape

    def hold_current_piece(self):
        if not self.can_hold:
            return
        if self.hold_piece is None:
            self.hold_piece = self.current_piece
            self.spawn_new_piece()
        else:
            self.hold_piece, self.current_piece = self.current_piece, self.hold_piece
            self.current_piece.x = BOARD_WIDTH // 2 - len(self.current_piece.shape[0]) // 2
            self.current_piece.y = 0
        self.can_hold = False

    def move(self, dx):
        if not self.check_collision(dx=dx):
            self.current_piece.x += dx

    def hard_drop(self):
        while not self.check_collision(dy=1):
            self.current_piece.y += 1
        self.merge_piece()
        self.check_lines()
        self.spawn_new_piece()

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, val in enumerate(row):
                if val:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.can_hold = True

    def check_lines(self):
        full_rows = []
        for i, row in enumerate(self.board):
            if all(cell != 0 for cell in row):
                full_rows.append(i)

        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [0] * BOARD_WIDTH)

        lines_cleared = len(full_rows)
        if lines_cleared > 0:
            self.lines += lines_cleared
            self.score += [40, 100, 300, 1200][lines_cleared - 1] * self.level
            self.level = 1 + self.lines // 10

    def draw_block(self, x, y, color, surface):
        pygame.draw.rect(surface, COLORS[color],
                         (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def draw_panel(self, surface, x, title, pieces):
        pygame.draw.rect(surface, WHITE, (x, 50, PANEL_WIDTH - 10, 180), 2)
        title_surf = self.font.render(title, True, WHITE)
        surface.blit(title_surf, (x + 10, 20))
        for i, piece in enumerate(pieces):
            if piece is None:
                continue
            shape = SHAPES[piece]
            color = piece + 1
            for y, row in enumerate(shape):
                for x_idx, val in enumerate(row):
                    if val:
                        self.draw_block(x // BLOCK_SIZE + x_idx + 2, i * 3 + y + 2, color, surface)

    def draw(self, screen):
        screen.fill(BLACK)

        # Ana tahta
        board_surface = pygame.Surface((WIDTH, HEIGHT))
        board_surface.fill(BLACK)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    self.draw_block(x, y, self.board[y][x], board_surface)

        if self.current_piece and not self.game_over:
            for y, row in enumerate(self.current_piece.shape):
                for x, val in enumerate(row):
                    if val:
                        self.draw_block(self.current_piece.x + x,
                                        self.current_piece.y + y,
                                        self.current_piece.color, board_surface)

        screen.blit(board_surface, (PANEL_WIDTH, 50))

        # Sol panel (Hold)
        hold_piece = [self.hold_piece] if self.hold_piece else []
        self.draw_panel(screen, 10, "Hold",
                        [p.color - 1 for p in hold_piece] if hold_piece else [])

        # Sağ panel (Next)
        self.draw_panel(screen, PANEL_WIDTH + WIDTH + 10, "Next", self.next_pieces[:5])

        # Bilgi paneli
        info_y = HEIGHT + 60
        screen.blit(self.font.render(f'Score: {self.score}', True, WHITE), (10, info_y))
        screen.blit(self.font.render(f'Level: {self.level}', True, WHITE), (10, info_y + 30))
        screen.blit(self.font.render(f'Lines: {self.lines}', True, WHITE), (10, info_y + 60))

        if self.game_over:
            game_over_text = self.font.render('GAME OVER!', True, (255, 0, 0))
            screen.blit(game_over_text, (PANEL_WIDTH + WIDTH // 2 - 80, HEIGHT // 2))


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT + 100))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()

    fall_speed = 1000
    last_fall = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        dt = current_time - last_fall

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.move(0)
                    game.current_piece.y += 1
                    if game.check_collision():
                        game.current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_c:
                    game.hold_current_piece()

        if not game.game_over:
            if dt > fall_speed:
                game.current_piece.y += 1
                if game.check_collision():
                    game.current_piece.y -= 1
                    game.merge_piece()
                    game.check_lines()
                    game.spawn_new_piece()
                last_fall = current_time
            fall_speed = max(50, 1000 - (game.level - 1) * 100)

        game.draw(screen)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
