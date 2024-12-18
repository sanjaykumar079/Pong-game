import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.get_caption()
FPS = 60 # frames for second
WHITE = (255, 255, 255)
BLACK = (0,0,0)
BLUE = (90, 236, 231, 1)
PEDDEL_WIDTH, PEDDEL_HEIGHT= 20 ,100
BALL_RAIDUS = 7
SCORE_FONT  = pygame.font.SysFont('comicsans', 50)
WINNING_SCORE =5


class Peddel:
  COLOR = BLUE
  VEL = 4
  def __init__(self, x, y, width, height):
    self.x = self.original_x = x
    self.y =self.original_y = y
    self.width = width
    self.height =height
  
  def draw(self, win):
    pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height ))

  def move(self, up = True):
    if up:
      self.y -= self.VEL
    else:
      self.y += self.VEL
    
  def reset(self):
    self.x = self.original_x
    self.y = self.original_y

class Ball:
  COLOR = WHITE
  MAX_VEL = 5
  def __init__(self, x,y,radius):
    self.x = self.original_x =  x
    self.y = self.original_y = y
    self.radius = radius
    self.x_vel = self.MAX_VEL
    self.y_vel = 0
    
  def draw(self, win):
    pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
  
  def move(self):
    self.x += self.x_vel
    self.y += self.y_vel
    
  def reset(self):
    self.x = self.original_x
    self.y = self.original_y
    self.x_vel *= -1
    self.y_vel = 0
    


def draw(win, peddels, ball, left_score, right_score):
  win.fill(BLACK) # it changes the background color of window
  left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
  right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
  win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
  win.blit(right_score_text, (WIDTH * (3/4) -
                              right_score_text.get_width()//2, 20))
  for peddel in peddels:
    peddel.draw(win)
    
  for i in range(10, HEIGHT, HEIGHT//20):
    if i % 2 == 1:
        continue
    pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
  ball.draw(win)
  pygame.display.update() #it updates the color of window
 
def handle_collision(ball, left_peddel, right_peddel):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_peddel.y and ball.y <= left_peddel.y + left_peddel.height:
            if ball.x - ball.radius <= left_peddel.x + left_peddel.width:
                ball.x_vel *= -1

                middle_y = left_peddel.y + left_peddel.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_peddel.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_peddel.y and ball.y <= right_peddel.y + right_peddel.height:
            if ball.x + ball.radius >= right_peddel.x:
                ball.x_vel *= -1

                middle_y = right_peddel.y + right_peddel.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_peddel.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
 
def handel_peddel_moment(keys, left_peddel, right_peddel):
  if keys[pygame.K_w] and left_peddel.y - left_peddel.VEL >= 0:
    left_peddel.move(up = True)
  if keys[pygame.K_s] and left_peddel.y + left_peddel.VEL + left_peddel.height <= HEIGHT:
    left_peddel.move(up=False)
  if keys[pygame.K_UP] and right_peddel.y - right_peddel.VEL >= 0:
    right_peddel.move(up=True)
  if keys[pygame.K_DOWN]  and right_peddel.y + right_peddel.VEL + right_peddel.height <= HEIGHT:
    right_peddel.move(up=False)

def main():
  run = True
  left_score = 0
  right_score = 0
  clock = pygame.time.Clock()
  left_peddel = Peddel(10, HEIGHT//2 - PEDDEL_HEIGHT //
                         2, PEDDEL_WIDTH, PEDDEL_HEIGHT)
  right_peddel = Peddel(WIDTH - 10 - PEDDEL_WIDTH, HEIGHT //
                          2 - PEDDEL_HEIGHT//2, PEDDEL_WIDTH, PEDDEL_HEIGHT)
  ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RAIDUS)
  while run:
    clock.tick(FPS) #this while loop can not run more than 60sec
    draw(WIN, [left_peddel, right_peddel] , ball, left_score, right_score)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break
      
    keys = pygame.key.get_pressed()
    handel_peddel_moment(keys, left_peddel, right_peddel)
    ball.move()
    handle_collision(ball, left_peddel, right_peddel)
    
    if ball.x < 0:
      right_score += 1
      ball.reset()
    elif ball.x > WIDTH:
        left_score += 1
        ball.reset()
        
    won = False
    if left_score > WINNING_SCORE:
      won = True
      win_text = "left player won!"

    elif right_score > WINNING_SCORE:
      won = True
      win_text = "right player won!"
      
    if won :
      text = SCORE_FONT.render(win_text, 1, WHITE)
      WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT //2 - text.get_height()//2))
      pygame.display.update()
      ball.reset()
      pygame.time.delay(5000)
      left_peddel.reset()
      right_peddel.reset()
      left_score = 0
      right_score = 0
    
  pygame.quit()
  
if __name__ == '__main__':
  main()