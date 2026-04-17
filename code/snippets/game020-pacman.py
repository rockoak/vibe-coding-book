import pygame
import random
import sys
import math
import time

# 初始化pygame和混音器
pygame.init()
pygame.mixer.init()

# 遊戲常數設定
SCREEN_WIDTH = 896  # 原版Pac-Man解析度比例
SCREEN_HEIGHT = 992
BLOCK_SIZE = 16  # 原版使用16x16像素塊
FPS = 60

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (33, 33, 222)

# 遊戲狀態
READY = 0
PLAYING = 1
DYING = 2
GAME_OVER = 3
LEVEL_COMPLETE = 4

# 原版迷宮設計 (更精確)
MAZE_LAYOUT = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## #      # ##.######",
    "      .   #      #   .      ",
    "######.## #      # ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####o#",
    "#...##.......  .......##...#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

class SpriteSheet:
    """精靈圖資源管理"""
    def __init__(self):
        self.sprites = {}
        self.create_sprites()

    def create_sprites(self):
        """創建遊戲中使用的所有精靈圖"""

        # 小精靈動畫幀 (8個方向 x 3個動畫幀)
        pacman_frames = []
        for direction in range(8):  # 8個方向
            frames = []
            for frame in range(3):  # 3個動畫幀
                # 創建小精靈圖形
                surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                center = (BLOCK_SIZE // 2, BLOCK_SIZE // 2)
                radius = BLOCK_SIZE // 2 - 1

                # 計算嘴巴角度
                mouth_angle = 45  # 嘴巴張開角度
                start_angle = (direction * 45 - mouth_angle + frame * 15) % 360
                end_angle = (direction * 45 + mouth_angle - frame * 15) % 360

                # 繪製圓餅形
                pygame.draw.circle(surface, YELLOW, center, radius)
                if frame < 2:  # 不繪製閉嘴幀
                    pygame.draw.polygon(surface, BLACK, [
                        center,
                        (center[0] + radius * math.cos(math.radians(start_angle)),
                         center[1] + radius * math.sin(math.radians(start_angle))),
                        (center[0] + radius * math.cos(math.radians(end_angle)),
                         center[1] + radius * math.sin(math.radians(end_angle)))
                    ])

                frames.append(surface)
            pacman_frames.append(frames)

        self.sprites['pacman'] = pacman_frames

        # 鬼魂動畫幀
        ghost_colors = [RED, PINK, CYAN, ORANGE]
        ghost_names = ['blinky', 'pinky', 'inky', 'clyde']

        for i, (color, name) in enumerate(zip(ghost_colors, ghost_names)):
            frames = []
            for frame in range(2):  # 2個動畫幀
                surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)

                # 身體
                pygame.draw.circle(surface, color, (BLOCK_SIZE//2, BLOCK_SIZE//2), BLOCK_SIZE//2 - 1)
                pygame.draw.rect(surface, color, (1, BLOCK_SIZE//2, BLOCK_SIZE-2, BLOCK_SIZE//2))

                # 波浪形底部
                for x in range(0, BLOCK_SIZE, 2):
                    pygame.draw.line(surface, color, (x, BLOCK_SIZE-1), (x+1, BLOCK_SIZE-1))

                # 眼睛
                eye_color = WHITE
                pupil_color = BLUE
                eye_y = BLOCK_SIZE // 3
                left_eye_x = BLOCK_SIZE // 3
                right_eye_x = 2 * BLOCK_SIZE // 3

                pygame.draw.circle(surface, eye_color, (left_eye_x, eye_y), 3)
                pygame.draw.circle(surface, eye_color, (right_eye_x, eye_y), 3)
                pygame.draw.circle(surface, pupil_color, (left_eye_x, eye_y), 1)
                pygame.draw.circle(surface, pupil_color, (right_eye_x, eye_y), 1)

                frames.append(surface)

            self.sprites[name] = frames

        # 豆子
        dot_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(dot_surface, WHITE, (BLOCK_SIZE//2, BLOCK_SIZE//2), 2)
        self.sprites['dot'] = dot_surface

        # 大豆子
        power_dot_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(power_dot_surface, WHITE, (BLOCK_SIZE//2, BLOCK_SIZE//2), 4)
        self.sprites['power_dot'] = power_dot_surface

        # 水果
        fruits = ['cherry', 'strawberry', 'orange', 'apple', 'melon', 'galaxian', 'bell', 'key']
        fruit_colors = [(255,0,0), (255,0,128), (255,165,0), (255,0,0), (0,255,0), (255,0,255), (255,255,0), (128,128,128)]

        for fruit, color in zip(fruits, fruit_colors):
            surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (BLOCK_SIZE//2, BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)
            self.sprites[fruit] = surface

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.direction = 0  # 0:右, 1:下, 2:左, 3:上
        self.next_direction = 0
        self.speed = 2
        self.animation_frame = 0
        self.animation_timer = 0
        self.dead = False

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = 0
        self.next_direction = 0
        self.dead = False

    def move(self, maze):
        # 嘗試改變方向
        if self.can_move(self.next_direction, maze):
            self.direction = self.next_direction

        # 移動
        if self.can_move(self.direction, maze):
            if self.direction == 0:  # 右
                self.x += self.speed
            elif self.direction == 1:  # 下
                self.y += self.speed
            elif self.direction == 2:  # 左
                self.x -= self.speed
            elif self.direction == 3:  # 上
                self.y -= self.speed

        # 處理邊界穿越
        if self.x < 0:
            self.x = len(maze[0]) * BLOCK_SIZE - BLOCK_SIZE
        elif self.x >= len(maze[0]) * BLOCK_SIZE:
            self.x = 0

        # 更新動畫
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_frame = (self.animation_frame + 1) % 3
            self.animation_timer = 0

    def can_move(self, direction, maze):
        # 檢查下一個位置是否可以移動
        next_x = self.x
        next_y = self.y

        if direction == 0:  # 右
            next_x += self.speed
        elif direction == 1:  # 下
            next_y += self.speed
        elif direction == 2:  # 左
            next_x -= self.speed
        elif direction == 3:  # 上
            next_y -= self.speed

        # 轉換為網格坐標
        grid_x = int(next_x // BLOCK_SIZE)
        grid_y = int(next_y // BLOCK_SIZE)

        # 檢查邊界
        if grid_x < 0 or grid_x >= len(maze[0]) or grid_y < 0 or grid_y >= len(maze):
            return False

        # 檢查是否是牆壁
        return maze[grid_y][grid_x] != '#'

    def draw(self, screen, sprites):
        if self.dead:
            return

        direction_frame = self.direction
        frame = self.animation_frame
        sprite = sprites.sprites['pacman'][direction_frame][frame]
        screen.blit(sprite, (self.x, self.y))

class Ghost:
    def __init__(self, x, y, color, name, personality):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.color = color
        self.name = name
        self.personality = personality  # 'chase', 'ambush', 'patrol', 'random'
        self.direction = random.randint(0, 3)
        self.speed = 1.5
        self.mode = "scatter"  # scatter, chase, frightened, eaten
        self.frightened_timer = 0
        self.animation_frame = 0
        self.animation_timer = 0
        self.target_x = 0
        self.target_y = 0
    def start_eaten(self):
        """當鬼被吃到時啟動: 播放大叫聲並啟動消失動畫"""
        # 播放大叫聲（假設sound_manager已經存在或全域）
        if hasattr(self, 'sound_scream'):
            self.sound_scream.play()
        elif 'sound_manager' in globals() and hasattr(sound_manager, 'scream'):
            sound_manager.scream.play()

        # 啟動消失動畫
        self.mode = 'eaten'
        self.eaten_fade_alpha = 255  # 初始完全不透明

    def update_eaten_disappear(self):
        """在eaten模式下慢慢消失──每次呼叫遞減alpha"""
        if self.mode == 'eaten':
            if not hasattr(self, 'eaten_fade_alpha'):
                self.eaten_fade_alpha = 255
            if self.eaten_fade_alpha > 0:
                self.eaten_fade_alpha -= 8  # 每一幀慢慢減少透明度
                if self.eaten_fade_alpha < 0:
                    self.eaten_fade_alpha = 0  # 不要小於0

    def draw(self, screen, sprites):
        if self.mode == 'eaten':
            # 畫半透明鬼魂
            direction_frame = self.direction
            frame = self.animation_frame
            sprite = sprites.sprites[self.name][direction_frame][frame].copy()  # copy避免污染原圖
            if not hasattr(self, 'eaten_fade_alpha'):
                self.eaten_fade_alpha = 255
            sprite.set_alpha(self.eaten_fade_alpha)
            screen.blit(sprite, (self.x, self.y))
            return
        # 如果不是被吃掉的狀態，照原本方式畫
        direction_frame = self.direction
        frame = self.animation_frame
        sprite = sprites.sprites[self.name][direction_frame][frame]
        screen.blit(sprite, (self.x, self.y))


    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = random.randint(0, 3)
        self.mode = "scatter"
        self.frightened_timer = 0

    def set_target(self, pacman, blinky=None):
        """設定鬼魂的目標位置"""
        if self.mode == "frightened":
            # 驚嚇模式：隨機移動
            self.target_x = random.randint(0, 27) * BLOCK_SIZE
            self.target_y = random.randint(0, 30) * BLOCK_SIZE
        elif self.mode == "scatter":
            # 分散模式：各回自己的角落
            corners = {
                'blinky': (27 * BLOCK_SIZE, 0),
                'pinky': (0, 0),
                'inky': (27 * BLOCK_SIZE, 30 * BLOCK_SIZE),
                'clyde': (0, 30 * BLOCK_SIZE)
            }
            self.target_x, self.target_y = corners.get(self.name, (13 * BLOCK_SIZE, 15 * BLOCK_SIZE))
        else:  # chase mode
            if self.personality == 'chase':  # Blinky - 直接追蹤
                self.target_x, self.target_y = pacman.x, pacman.y
            elif self.personality == 'ambush':  # Pinky - 埋伏
                if pacman.direction == 0:  # 右
                    self.target_x = pacman.x + 4 * BLOCK_SIZE
                    self.target_y = pacman.y
                elif pacman.direction == 1:  # 下
                    self.target_x = pacman.x
                    self.target_y = pacman.y + 4 * BLOCK_SIZE
                elif pacman.direction == 2:  # 左
                    self.target_x = pacman.x - 4 * BLOCK_SIZE
                    self.target_y = pacman.y
                else:  # 上
                    self.target_x = pacman.x
                    self.target_y = pacman.y - 4 * BLOCK_SIZE
            elif self.personality == 'patrol':  # Inky - 使用Blinky位置計算
                if blinky:
                    if pacman.direction == 0:  # 右
                        pivot_x = pacman.x + 2 * BLOCK_SIZE
                        pivot_y = pacman.y
                    elif pacman.direction == 1:  # 下
                        pivot_x = pacman.x
                        pivot_y = pacman.y + 2 * BLOCK_SIZE
                    elif pacman.direction == 2:  # 左
                        pivot_x = pacman.x - 2 * BLOCK_SIZE
                        pivot_y = pacman.y
                    else:  # 上
                        pivot_x = pacman.x
                        pivot_y = pacman.y - 2 * BLOCK_SIZE

                    # 計算向量
                    vector_x = pivot_x - blinky.x
                    vector_y = pivot_y - blinky.y
                    self.target_x = pivot_x + vector_x
                    self.target_y = pivot_y + vector_y
                else:
                    self.target_x, self.target_y = pacman.x, pacman.y
            else:  # Clyde - 隨機但有點追蹤
                distance = math.sqrt((pacman.x - self.x)**2 + (pacman.y - self.y)**2)
                if distance > 8 * BLOCK_SIZE:
                    self.target_x, self.target_y = pacman.x, pacman.y
                else:
                    self.target_x = random.randint(0, 27) * BLOCK_SIZE
                    self.target_y = random.randint(0, 30) * BLOCK_SIZE

    def move(self, maze, pacman, blinky=None):
        # 更新模式和計時器
        if self.mode == "frightened":
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = "chase"

        # 設定目標
        self.set_target(pacman, blinky)

        # 尋路演算法 (簡化版A*)
        directions = [(0, -self.speed), (self.speed, 0), (0, self.speed), (-self.speed, 0)]  # 上、右、下、左
        best_direction = self.direction
        min_distance = float('inf')

        for i, (dx, dy) in enumerate(directions):
            # 檢查是否可以反向移動 (鬼魂不能立即反向)
            if abs(i - self.direction) == 2:
                continue

            next_x = self.x + dx
            next_y = self.y + dy
            grid_x = int(next_x // BLOCK_SIZE)
            grid_y = int(next_y // BLOCK_SIZE)

            if (0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze) and
                maze[grid_y][grid_x] != '#'):
                distance = math.sqrt((next_x - self.target_x)**2 + (next_y - self.target_y)**2)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = i

        self.direction = best_direction

        # 移動
        dx, dy = directions[self.direction]
        self.x += dx
        self.y += dy

        # 更新動畫
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

    def draw(self, screen, sprites):
        sprite = sprites.sprites[self.name][self.animation_frame]
        screen.blit(sprite, (self.x, self.y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("小精靈豪華版 - Pac-Man Deluxe")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # 載入精靈圖
        self.sprites = SpriteSheet()

        # 初始化遊戲物件
        self.pacman = Pacman(13.5 * BLOCK_SIZE, 23 * BLOCK_SIZE)
        self.ghosts = [
            Ghost(13.5 * BLOCK_SIZE, 11 * BLOCK_SIZE, RED, 'blinky', 'chase'),
            Ghost(11.5 * BLOCK_SIZE, 14 * BLOCK_SIZE, PINK, 'pinky', 'ambush'),
            Ghost(13.5 * BLOCK_SIZE, 14 * BLOCK_SIZE, CYAN, 'inky', 'patrol'),
            Ghost(15.5 * BLOCK_SIZE, 14 * BLOCK_SIZE, ORANGE, 'clyde', 'random')
        ]

        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.level = 1
        self.game_state = READY
        self.ready_timer = 180  # 3秒準備時間
        self.fruit_timer = 0
        self.fruit_visible = False
        self.fruit_type = 0

        # 載入音效 (簡化版)
        self.eat_dot_sound = None
        self.eat_fruit_sound = None
        self.death_sound = None

        # 初始化迷宮
        self.maze = self.create_maze()
        self.dots_remaining = self.count_dots()

    def create_maze(self):
        """根據佈局字串創建迷宮"""
        maze = []
        for row in MAZE_LAYOUT:
            maze_row = []
            for char in row:
                if char == '#':
                    maze_row.append('#')
                elif char == '.':
                    maze_row.append('.')
                elif char == 'o':
                    maze_row.append('o')
                else:
                    maze_row.append(' ')
            maze.append(maze_row)
        return maze

    def count_dots(self):
        """計算剩餘豆子數量"""
        count = 0
        for row in self.maze:
            for cell in row:
                if cell in ['.', 'o']:
                    count += 1
        return count

    def draw_maze(self):
        """繪製迷宮"""
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                screen_x = x * BLOCK_SIZE
                screen_y = y * BLOCK_SIZE

                if cell == '#':  # 牆壁
                    # 繪製藍色牆壁
                    pygame.draw.rect(self.screen, DARK_BLUE,
                                   (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE))
                elif cell == '.':  # 小豆子
                    self.screen.blit(self.sprites.sprites['dot'], (screen_x, screen_y))
                elif cell == 'o':  # 大豆子
                    self.screen.blit(self.sprites.sprites['power_dot'], (screen_x, screen_y))

        # 繪製水果
        if self.fruit_visible:
            fruit_names = ['cherry', 'strawberry', 'orange', 'apple', 'melon', 'galaxian', 'bell', 'key']
            fruit_x = 13.5 * BLOCK_SIZE
            fruit_y = 17 * BLOCK_SIZE
            self.screen.blit(self.sprites.sprites[fruit_names[self.fruit_type]], (fruit_x, fruit_y))

    def check_collision(self):
        """檢查碰撞"""
        if self.game_state != PLAYING:
            return

        # 檢查吃豆子
        pacman_grid_x = int((self.pacman.x + BLOCK_SIZE//2) // BLOCK_SIZE)
        pacman_grid_y = int((self.pacman.y + BLOCK_SIZE//2) // BLOCK_SIZE)

        if 0 <= pacman_grid_x < len(self.maze[0]) and 0 <= pacman_grid_y < len(self.maze):
            cell = self.maze[pacman_grid_y][pacman_grid_x]
            if cell == '.':  # 小豆子
                self.maze[pacman_grid_y][pacman_grid_x] = ' '
                self.score += 10
                self.dots_remaining -= 1
            elif cell == 'o':  # 大豆子
                self.maze[pacman_grid_y][pacman_grid_x] = ' '
                self.score += 50
                self.dots_remaining -= 1
                # 讓所有鬼魂進入驚嚇模式
                for ghost in self.ghosts:
                    ghost.mode = "frightened"
                    ghost.frightened_timer = 600  # 10秒

        # 檢查與鬼魂碰撞
        for ghost in self.ghosts:
            if self.game_state == DYING:
                continue

            distance = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
            if distance < BLOCK_SIZE:
                if ghost.mode == "frightened":
                    # 吃掉鬼魂
                    ghost.reset()
                    self.score += 200
                else:
                    # 小精靈死亡
                    self.game_state = DYING
                    self.pacman.dead = True
                    break

    def update_fruit(self):
        """更新水果顯示"""
        self.fruit_timer += 1

        # 水果出現時間
        if self.dots_remaining <= 170 and not self.fruit_visible:
            self.fruit_visible = True
            self.fruit_timer = 0
        elif self.fruit_visible and self.fruit_timer >= 600:  # 10秒
            self.fruit_visible = False

        # 檢查吃水果
        if self.fruit_visible:
            fruit_x = 13.5 * BLOCK_SIZE
            fruit_y = 17 * BLOCK_SIZE
            distance = math.sqrt((self.pacman.x - fruit_x)**2 + (self.pacman.y - fruit_y)**2)
            if distance < BLOCK_SIZE:
                fruit_values = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
                self.score += fruit_values[self.fruit_type]
                self.fruit_visible = False

    def check_level_complete(self):
        """檢查關卡完成"""
        return self.dots_remaining == 0

    def next_level(self):
        """進入下一關"""
        self.level += 1
        self.fruit_type = min(self.fruit_type + 1, 7)  # 水果升級
        self.game_state = LEVEL_COMPLETE

        # 重置迷宮
        self.maze = self.create_maze()
        self.dots_remaining = self.count_dots()

        # 重置所有角色
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()

    def draw_ui(self):
        """繪製用戶界面"""
        # 分數
        score_text = self.font.render(f"分數: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 最高分
        high_score_text = self.font.render(f"最高分: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (10, 50))

        # 關卡
        level_text = self.font.render(f"關卡: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 90))

        # 生命
        for i in range(self.lives):
            pygame.draw.circle(self.screen, YELLOW, (SCREEN_WIDTH - 50 - i * 30, 30), 10)

        # 準備文字
        if self.game_state == READY:
            ready_text = self.font.render("準備開始!", True, YELLOW)
            self.screen.blit(ready_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        # 遊戲結束
        elif self.game_state == GAME_OVER:
            game_over_text = self.font.render("遊戲結束!", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            restart_text = self.small_font.render("按R重新開始", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

        # 關卡完成
        elif self.game_state == LEVEL_COMPLETE:
            level_complete_text = self.font.render(f"關卡 {self.level-1} 完成!", True, YELLOW)
            self.screen.blit(level_complete_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

    def run(self):
        """主遊戲循環"""
        running = True
        while running:
            self.screen.fill(BLACK)

            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pacman.next_direction = 2
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.next_direction = 0
                    elif event.key == pygame.K_UP:
                        self.pacman.next_direction = 3
                    elif event.key == pygame.K_DOWN:
                        self.pacman.next_direction = 1
                    elif event.key == pygame.K_r and self.game_state == GAME_OVER:
                        # 重新開始
                        self.score = 0
                        self.lives = 3
                        self.level = 1
                        self.game_state = READY
                        self.ready_timer = 180
                        self.maze = self.create_maze()
                        self.dots_remaining = self.count_dots()
                        self.pacman.reset()
                        for ghost in self.ghosts:
                            ghost.reset()
                    elif event.key == pygame.K_SPACE and self.game_state == LEVEL_COMPLETE:
                        self.game_state = READY
                        self.ready_timer = 180
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # 更新遊戲邏輯
            if self.game_state == READY:
                self.ready_timer -= 1
                if self.ready_timer <= 0:
                    self.game_state = PLAYING

            elif self.game_state == PLAYING:
                self.pacman.move(self.maze)
                blinky = self.ghosts[0] if len(self.ghosts) > 0 else None
                for ghost in self.ghosts:
                    ghost.move(self.maze, self.pacman, blinky)

                self.check_collision()
                self.update_fruit()

                if self.check_level_complete():
                    self.next_level()

            elif self.game_state == DYING:
                # 死亡動畫 (簡化)
                pygame.time.wait(2000)
                self.lives -= 1
                if self.lives > 0:
                    self.game_state = READY
                    self.ready_timer = 180
                    self.pacman.reset()
                    for ghost in self.ghosts:
                        ghost.reset()
                else:
                    self.game_state = GAME_OVER
                    self.high_score = max(self.high_score, self.score)

            # 繪製遊戲
            self.draw_maze()
            if self.game_state in [READY, PLAYING, LEVEL_COMPLETE]:
                self.pacman.draw(self.screen, self.sprites)
                for ghost in self.ghosts:
                    ghost.draw(self.screen, self.sprites)

            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
