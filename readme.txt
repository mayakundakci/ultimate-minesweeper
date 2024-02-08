My project is the classic Minesweeper game! 

The player can play the game in four different difficulty levels: easy, medium, hard, and extreme.
The ultimate goal is to reveal all non-mine tiles (by left-clicking). If a mine is clicked, the 
game is lost. The player can get help from the hint function (which will guide them to cells 
where moves can be made, or highlight wrong flags,) and when the game is won they can save 
their scores to the leaderboard. 


How to run:
    1. Make sure PIL/Pillow and cmu_graphics installed. Refer to the following link if not:
     https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#installingModules


    2. Download the code into a folder.


    3. Download the CSV file ‘highscores.csv’ into the same folder


    4. Download all images (listed below) into the same folder:
        pink.png
        myPink.png
        sakura.png
        clock.png 
        exit.png 
        flagg.png 
        helpscreen.png 
        mine.png 
        restart.png 
        wrong.png 
        trophy.png 


    5. The user can change the start screen to different screens by changing the “start” screen
       in runAppWithScreens(“start”) to any of the following:
        “game”
        “help” 
        “leaderboard”
        “saveScore”


    6. Run the file in an editor

Libraries Needed:
	PIL/Pillow
    cmu_graphics

