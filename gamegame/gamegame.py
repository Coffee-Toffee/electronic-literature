####
# Flappy Bird
# What is a game, if not text?
# by: Luna Harrison
# sorry for the hard coding, but it's a stylistic choice 
####

from py5 import Sketch
import random
from playsound import playsound
class Game(Sketch):
    
    def __init__(self):
        # Call the parent (Sketch) class's __init__() method
        super().__init__()  
        #starting values
        self.player_x = 400
        self.player_y = 400
        self.y_velocity = 0
        self.player_speed = 5
        self.pipe_list_len = 5
        self.pipes = []
        self.game_speed = 4
        self.score = 0
        for i in range(1, self.pipe_list_len+1):  #create the pipes
            x_offset = random.randint(0, 420)
            y_offset = random.randint(-300, 350)
            self.add_pipe(2000+ i * 1000 + x_offset, y_offset + 600 , 700 + random.randint(-50, 50), i)

    def settings(self):
        self.size(1920, 1080)

    def setup(self):
        self.bird = self.load_image('bird.png')
        self.pipes_img = self.load_image('pipe.png')
        self.death_img = self.load_image('death.png')
        self.rect_mode(self.CENTER)
        self.frame_rate(60)
        self.background(0)
        self.text_size(20)
        self.text("Welcome to Flappy Bird", 500, 500)
        self.text("Controls are: 'a' to move left and 'd' to move right, and click any mouse button to flap.", 500, 600)
   
    def jump(self):
        self.y_velocity += -7

    def mouse_pressed(self):
        self.jump()
    
    def game_over(self):
        #end the game
        self.background(0)
        self.text("Game Over", 1920//2, 520)
        self.text("Your Score: " + str((self.score)), 1920//2, 560)
        print(1/0)

    def gravity(self):
        self.y_velocity += 0.3
        self.player_y += self.y_velocity

    def add_pipe(self, initial_x, top_y, gap, index_value, state = 0):
        self.pipes.append([initial_x, top_y, gap, index_value, state])
    
    def draw_pipes(self):
        for pipe in self.pipes:
            if pipe[0] - self.game_speed* self.frame_count < 1950:
                self.draw_pipe(pipe[0]-self.game_speed*self.frame_count, pipe[1], pipe[2])

    def draw_pipe(self, x, y, gap):
        self.image(self.pipes_img, x, y, 128, 512)
        self.image(self.pipes_img, x, y+486, 128, 512)
        self.image(self.pipes_img, x, y - gap, 128, 512)
        self.image(self.pipes_img, x, y - gap - 486, 128, 512)
    
    def collision_check(self): 
        for pipe in self.pipes:
            #scoring
            if pipe[0] - self.game_speed* self.frame_count < self.player_x - 50 and pipe[4] == 0:
                self.score += 1
                pipe[4] = 1
                playsound('ding1.mp3', False)
            #checks if the pipe is offscreen, and if so, removes it, and spawns a new one
            if pipe[0] - self.game_speed* self.frame_count < 0: 
                self.add_pipe(pipe[0] + self.pipe_list_len*1000 + random.randint(0, 200), 
                pipe[1] + random.randint(-40, 40), pipe[2] + random.randint(-20,20), pipe[3])
                self.pipes.remove(pipe)
            #collision 
            if pipe[0] - self.game_speed* self.frame_count < 1950:
                if (self.player_x - 40 < pipe[0]- self.game_speed* self.frame_count < self.player_x + 40 and 
                    self.player_y - 440 < pipe[1] < self.player_y + 45):
                    
                    self.game_over()
                
                if (self.player_x - 40 < pipe[0]- self.game_speed* self.frame_count < self.player_x + 40 and 
                    self.player_y - 440 < pipe[1] - pipe[2] < self.player_y + 45):
                    
                    self.game_over()

    def draw(self):
        if self.frame_count > 60*4:
            
            self.background(0)
            self.collision_check()
            
            self.text("Score: " + str((self.score)), 1800, 50)

            if self.player_y > 1000 or self.player_y < -40: 
                self.game_over()
             
            self.image(self.death_img, self.width/2, -50, 1024, 128)
            self.image(self.death_img, 0, -50, 1024, 128)
            
            self.image(self.death_img, self.width/2, self.height - 80, 1024, 128)
            self.image(self.death_img, 0, self.height - 80, 1024, 128)
            
            self.gravity()
            
            self.image(self.bird, self.player_x, self.player_y, 128, 128)

            self.draw_pipes()
           
            self.game_speed += 0.001 

            if self.is_key_pressed:
                if self.key == 'a':
                    self.player_x -= self.player_speed
                if self.key == 'd':
                    self.player_x += self.player_speed

gaming = Game()
gaming.run_sketch()
