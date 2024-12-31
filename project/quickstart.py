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

class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        circle.next_to(square, RIGHT, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen

        self.wait(1)

class HelloWorld(Scene):
    def construct(self):
        # Create Text object
        hello = Text("Hello, World!")
        # Display text
        self.play(Write(hello),run_time=2)
        self.wait(1)