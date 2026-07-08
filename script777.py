import pygame
import math
import sys

# ==================== Класс HardDrive ====================
class HardDrive:
    def __init__(self, cx, cy, radius):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.sectors = [False] * 8          # False – пусто, True – занято
        self.fill_color = (0, 0, 255)       # синий

    def draw(self, surface):
        # Внешняя окружность
        pygame.draw.circle(surface, (0, 0, 0), (self.cx, self.cy), self.radius, 2)
        # Проходим по каждому сектору
        for i in range(8):
            angle = math.radians(i * 45)
            next_angle = math.radians((i + 1) * 45)
            if self.sectors[i]:
                # Заливаем сектор синим
                p1 = (self.cx, self.cy)
                p2 = (self.cx + self.radius * math.cos(angle),
                      self.cy + self.radius * math.sin(angle))
                p3 = (self.cx + self.radius * math.cos(next_angle),
                      self.cy + self.radius * math.sin(next_angle))
                pygame.draw.polygon(surface, self.fill_color, [p1, p2, p3])
            # Рисуем линию-границу
            x = self.cx + self.radius * math.cos(angle)
            y = self.cy + self.radius * math.sin(angle)
            pygame.draw.line(surface, (0, 0, 0), (self.cx, self.cy), (x, y), 1)

    def write_sector(self):
        for i in range(8):
            if not self.sectors[i]:
                self.sectors[i] = True
                return True
        return False

    def clear(self):
        for i in range(8):
            self.sectors[i] = False

    def is_full(self):
        return all(self.sectors)


# ==================== Инициализация Pygame ====================
pygame.init()
screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Управление жёстким диском")
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

# Глобальные объекты
hard_drive = HardDrive(350, 300, 150)      # центр диска

# Прямоугольники вкладок
tab_rects = [
    pygame.Rect(10, 10, 150, 40),
    pygame.Rect(170, 10, 150, 40)
]
tab_labels = ["Управление", "Статус"]
active_tab = 0

# Кнопки на вкладке "Управление"
btn_write = pygame.Rect(50, 80, 200, 50)
btn_clear = pygame.Rect(300, 80, 200, 50)
btn_write_enabled = True
disk_full = False


# ==================== Функции отрисовки ====================
def draw_tabs():
    for i, rect in enumerate(tab_rects):
        color = (200, 200, 200) if i != active_tab else (100, 150, 255)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text = font.render(tab_labels[i], True, (0, 0, 0))
        screen.blit(text, (rect.x + 10, rect.y + 8))


def draw_buttons():
    if active_tab == 0:
        # Кнопка "Записать сектор"
        color = (100, 200, 100) if btn_write_enabled else (150, 150, 150)
        pygame.draw.rect(screen, color, btn_write)
        pygame.draw.rect(screen, (0, 0, 0), btn_write, 2)
        text = font.render("Записать сектор", True, (0, 0, 0))
        screen.blit(text, (btn_write.x + 10, btn_write.y + 10))
        # Кнопка "Очистить диск"
        pygame.draw.rect(screen, (200, 100, 100), btn_clear)
        pygame.draw.rect(screen, (0, 0, 0), btn_clear, 2)
        text = font.render("Очистить диск", True, (0, 0, 0))
        screen.blit(text, (btn_clear.x + 10, btn_clear.y + 10))
    else:
        # Статусная информация
        filled = sum(hard_drive.sectors)
        info = f"Занято секторов: {filled} / 8"
        text = font.render(info, True, (0, 0, 0))
        screen.blit(text, (50, 80))
        if disk_full:
            warn = font.render("Диск заполнен!", True, (255, 0, 0))
            screen.blit(warn, (50, 120))


# ==================== Главный цикл ====================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            # Переключение вкладок
            for i, rect in enumerate(tab_rects):
                if rect.collidepoint(pos):
                    active_tab = i
            # Если активна вкладка "Управление"
            if active_tab == 0:
                if btn_write.collidepoint(pos) and btn_write_enabled:
                    if hard_drive.write_sector():
                        if hard_drive.is_full():
                            btn_write_enabled = False
                            disk_full = True
                if btn_clear.collidepoint(pos):
                    hard_drive.clear()
                    btn_write_enabled = True
                    disk_full = False

    # Отрисовка
    screen.fill((255, 255, 255))
    draw_tabs()
    hard_drive.draw(screen)    # рисуем диск с секторами
    draw_buttons()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()