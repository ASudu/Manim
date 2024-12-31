from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        
        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate the square by 45 degrees

        self.play(Create(square))  # show the square on screen
        self.play(Transform(square, circle))  # transform the square into a circle
        self.play(FadeOut(square))  # fade out the square