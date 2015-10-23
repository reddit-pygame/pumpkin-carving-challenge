#Caching Pumpkins 

This challenge focuses on implementing my favorite digital art tool: Ctrl-Z. The included code allows the user to "carve" a jack-o-lantern by drawing over it. There's also a spooktastic splash screen to help get you in the Halloween spirit.

Github repo: https://github.com/reddit-pygame/pumpkin-carving-challenge

Reddit Challenge thread: 

##How it works

The user uses the mouse to draw in black on an "intermediary" surface, Pumpkin.work_surf, which is filled with and [color-keyed](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_colorkey) to white. This surface is blitted 
on top of the pumpkin image onto another surface, Pumkin.final, which is color-keyed to black. This results in the areas drawn by the user becoming transparent and exposing the 
background surface underneath (which changes color to give the illusion of flickering candlelight). This program uses /u/bitcraft's [animation module](https://github.com/bitcraft/animation) to achieve various 
animation and timing effects (especially in the splash screen). Though you shouldn't need it to complete the challenge, I highly recommend checking it out if you haven't - it will be a great addition to your bag of pygame tricks.

NOTE: This program starts in fullscreen mode by default. This may not work correctly on all platforms; you can change this behavior by removing the pg.FULLSCREEN argument to display.set_mode (in prepare.py) 
and setting StateEngine.fullscreen to False (in state_engine.py).

##Controls

Mouse Down - Start drawing

Mouse Up - Stop drawing

Up Arrow - Increase brush size

Down Arrow - Decrease brush size

F - Toggle fullscreen

ESC - Exit

#Challenge

Implement "undo" functionality. Each time the user begins to draw, the current state of the user's drawing should be saved. Pressing CTRL+z should allow the user to undo what was drawn previously. 
Pressing Ctrl+z multiple times should eventually undo all the user's drawing. [Surface.copy](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.copy) will probably come in handy for this.

##Achievements

**Cookie Cutter** - Allow the user to choose from predefined shapes to draw with

**Bring out the GIMP** - Allow the user to draw a black-and-white image with the image editor of their choice (like GIMP, paint.net, etc.) and place it on the jack-o-lantern. All images in resources/graphics are automatically colorkeyed to white.

#Happy Halloween!