# Necessary for pygame zero
import pgzrun
import random
# Used for Quitting the Program
import sys

# Window Properties
#   These create the size and name of the game
TITLE = 'Covid Catcher'
WIDTH = 600
HEIGHT = 600

# Title screen as an actor
# From Space Game 
game = Actor('game-title_final')

# Creates indexed game states for the different screens
game.state = ['title', 'game', 'game-over', 'about']
game.current_state = game.state[0]

# Creates an interactive character
survivor = Actor('alive3')

# Positions the character in the game window
survivor.pos = (100,560)
survivor.current_frame = 0
survivor.alive = True

# Plays the background music throughout the game
music.play('bg_music.wav')

# References a list of falling sanitizers and covid
# From Falling Zombies, changed to 'covid' and 'clean'
covid = []
clean = []

# Sets the initial scores at 0 when the game opens
score = 0
high_score = 0

#Draws background Screen
def draw_background():
    screen.blit('real_bg', (0,0))
    
#Draws Title Screen
def draw_title_screen():
    screen.blit('game-title_final', (0, 0))
    
#Draws Game Over Screen
#Space Game, changed by using 'death 3' and game-over  
def draw_game_over():
    screen.blit('game-over_final', (0, 0))
    survivor.draw()
    survivor.image = 'death 3'

#Draws About Screen
#Space Game, changed by using 'about_final'   
def draw_about():
    screen.blit('about_final', (0, 0))

# Draw covid virus fallings
#Space Game, changed by using 'tumor1' which is Covid, bad items
def draw_covid():
    global covid
    for tumor1 in covid:
        tumor1.draw()

# Draw sanitizer fallings
#Space Game, changed by using 'sanitzer1' which is good item
def draw_clean():
    global clean
    for sanitizer1 in clean:
        sanitizer1.draw()
        
# Draw function provided by pygame zero
def draw():
    
# Draws in the background picture starting at (0,0)
    draw_background()
    
# Show the main menu based on the game's "state"
    if game.current_state == 'title':
        draw_title_screen()
    
    # Draw the player and falling items when we are
    #  actively playing the game
    elif game.current_state == 'game':
        draw_covid()
        draw_clean()
        survivor.draw()
    
    # Forms game over screen for when player loses
    elif game.current_state == 'game-over':
        draw_game_over()
    
    # forms about screen
    elif game.current_state == 'about':
        draw_about()
    
    # keeps track of score and updates high score
    screen.draw.text('SCORE: ' + str(score), (5,5))
    screen.draw.text('HIGH SCORE: ' + str(high_score), (5, 22))

# checks if player hits either covid or sanitizer
# From Space Game, changed by using different iamges,
#   sounds, and names to fit this game, and by adding
#   an additional 'for' loop
def check_player_collisions():
    global score
    global covid
    global clean
    # Check all covid molecules
    for tumor1 in covid:
        # Did the player hit the molecule?
        if survivor.colliderect(tumor1):
            # Survivor is no longer alive, so he can't move
            #and is the 'dead' image
            survivor.alive = False
            survivor.image = 'death 3'
            #game state changes to game over
            game.current_state = game.state[2]
            # Play the explosion sound
            sounds.death.play()
            # Stop spawning covid and sanitizers
            clock.unschedule(spawn_covid)
            clock.unschedule(spawn_clean)
            # Empty the covid and clean lists
            covid = []
            clean = []
    # Check all sanitizers
    for sanitizer1 in clean:
        # Did the player hit the sanitizer?
        if survivor.colliderect(sanitizer1):
            sanitizer1.alive = False
            # Play the good 'ding' sound
            sounds.bleep.play()
            # increases your score by 1
            score += 1
    

# This function runs ~60 times every second
#   dt is a parameter that holds the amount of
#   time since the last call to update (delta time)
def update(dt):
    # Get the covid and clean list variable
    global covid
    global clean
    global score
    global high_score
    
    # Call our check_keys function
    #   to see if any keyboard keys are pressed
    check_keys(dt)
    
    # Call our function to move the covid molecules and sanitizers
    move_covid(dt)
    move_clean(dt)
    
    # Call our function to check if the player
    #caught covid or sanitizers
    check_player_collisions()
    
    # Remove any covid molecules and sanitizers
    #that are no longer on screen
    covid = covid_cleanup()
    clean = clean_cleanup()
    
    # Update the new high score if necessary
    if score > high_score:
        high_score = score
    
# Function updates the position of the covid molecules
#From Falling Zombies, changed names as well as the
#speed at which the image falls. Also adds a conditional
#for if covid is 'alive'.
def move_covid(dt):
    # Get the covid list variable
    global covid
    # Loop over all the covid molecules in the list
    for tumor1 in covid:
        # Add to the y position (covid molecule
        #   moving down)
        tumor1.y += dt * 150
        # Check if the covid molecule is off screen
        if tumor1.y > HEIGHT + 100:
            # Mark it as safe to cleanup
            tumor1.alive = False
            
#Function updates the position of the sanitizers
# From Falling Zombies (see detailed comments for move_covid)
def move_clean(dt):
    global clean
    # Loop over all the sanitizers in the list
    for sanitizer1 in clean:
        # Add to the y position (sanitizer
        #   moving down)
        sanitizer1.y += dt * 150
        # Check if the sanitizer is off screen
        if sanitizer1.y > HEIGHT + 100:
            # Mark it as safe to cleanup
            sanitizer1.alive = False
     
#Falling Zombies Game, changed by 'spawning' up sanitizer and Covid            
def spawn_covid():
    # Get the covid list variable
    global covid
    
    # Use random.randint to get a random number
    #   between the width of the game window with
    #   a 50 pixel buffer on either side
    xpos = random.randint(50, WIDTH-50)
    
    # Create covid actor
    tumor1 = Actor('tumor1')
    
    # Set the covid actors position to be off screen
    #   (at the top) and set the x value to be the
    #   randomly generated value
    tumor1.pos = (xpos, -50)
    
    # Add a property to set the covid to start
    #   "alive" so we don't clean it up by accident
    tumor1.alive = True
    
    # Append (add) our covid to the end of the list
    #   of other covid objects
    covid.append(tumor1)
 
# Falling Zombies Game, changed by using 'sanitizer1'
def spawn_clean():
    # Get the sanitizer list variable
    global clean
    
    # Use random.randint to get a random number
    #   between the first and second arguments
    xpos = random.randint(50, WIDTH-50)
    
    # Create sanitizer actor
    sanitizer1 = Actor('sanitizer1')

    
    # Set the sanitizer actors position to be off screen
    #   (at the top) and set the x value to be the
    #   randomly generated value
    sanitizer1.pos = (xpos, -50)

    # Add a property to set the sanitizer to start
    #   "alive" so we don't clean it up my accident
    sanitizer1.alive = True
    
    
    # Append (add) our sanitizer to the end of the list
    #   of other sanitizer objects
    clean.append(sanitizer1)
   
# Function to delete sanitizers that are off screen
# Falling Zombies Game, changed by 'cleaning' up sanitizer
def covid_cleanup():
    # Get the covid list variable
    global covid
    
    # Create a new empty list
    new_list = []
    
    # Get each covid from the list of covid molecules
    for tumor1 in covid:
        # Check if the covid is "alive"
        #   since alive is True or False this
        #   condition is valid
        if tumor1.alive:
            new_list.append(tumor1)
    
    # Return the new list without the covids that
    #   are not alive
    return new_list

# Function to delete covids that are off screen
# Falling Zombies Game, changed by 'cleaning' up Covid
def clean_cleanup():
    # Get the sanitizers list variable
    global clean
    
    # Create a new empty list
    new_list = []
    
    # Get each sanitizer from the list of sanitizers
    for sanitizer1 in clean:
        # Check if the sanitizer is "alive"
        #   since alive is True or False this
        #   condition is valid
        if sanitizer1.alive:
            new_list.append(sanitizer1)
    
    # Return the new list without the sanitizers that
    #   are not alive
    return new_list


# Function provided by pygame zero to check for keyboard presses
#with game over, covid cleaning, and sanitizer cleaning
def check_keys(key):
    global score
    # checks game state
    if game.current_state == 'title' or game.current_state == 'game-over' or game.current_state == 'about':
        # checks if Enter key is pressed
        if keyboard.RETURN:
            # Change the state to be "game"
            game.current_state = game.state[1]
            # Start covid spawning every 1 seconds
            clock.schedule_interval(spawn_covid, 1)
            # Start sanitizer1 spawning every 0.8 seconds
            clock.schedule_interval(spawn_clean, 0.8)
            # Resets survivor to alive image
            survivor.alive = True
            survivor.image = 'alive3'
            # Resets score to 0
            score = 0
        # starts the game
        draw()
    # checks if game state is 'game' (if survivor is alive)
    if game.current_state == 'game':
            #checks if the left arrow key is pressed
            if keyboard.left:
                # Move the survivor to the left
                survivor.x -= key * 175
                # stops the survivor from moving off the game screen
                if survivor.left < 0:
                        survivor.left = 0
            # Checks if the right arrow key is pressed
            if keyboard.right:
                # Move the survivor to the right
                survivor.x += key * 175
                # stops the survivor from moving off the game screen
                if survivor.right > WIDTH:
                    survivor.right = WIDTH
    
    #Checks if game state is 'about'
    if game.current_state == 'about':
        # checks if Backspace key is pressed
        if keyboard.BACKSPACE:
            #Goes to Title screen
            game.current_state = 'title'
        
    # Checks game state
    if game.current_state == 'title' or game.current_state == 'game-over':
        # checks if Space key is pressed
        if keyboard.SPACE:
            #Goes to About screen
            game.current_state = game.state[3]

    # Check for escape key press
    if keyboard.ESCAPE:
      # Exit the program
        sys.exit()
   
# Start pygame zero
pgzrun.go()

#Inspiration Site for Creating a Logo: https://placeit.net/logo-maker
#Character and Background Image: https://opengameart.org
#Covid and Sanitizer: https://game-icons.net
#Sounds and Music: https://sampleswap.org/index.php

