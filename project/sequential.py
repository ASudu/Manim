from manim import *

class Sequential(Scene):
    def construct(self):
        # Make a circle
        circle = Circle(radius=1)
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))
        self.wait(1)

        # Move the circle
        self.play(circle.animate.shift(LEFT))
        text = Text("Circle of radius 1", font_size=36)
        text.next_to(circle, RIGHT, buff=0.2)
        self.play(Write(text))
        self.wait(2)

        # Remove the text
        self.play(FadeOut(text))
        self.wait(1)

        # Move the cirle back to center
        self.play(circle.animate.shift(RIGHT))
        self.wait(1)

        # Create a square
        square = Square(side_length=2)
        square.set_fill(BLUE, opacity=0.5)

        # Transform the circle into a square
        self.play(Transform(circle, square))
        self.wait(1)

        # Move the square
        # NOTE: Since the circle was transformed into a square, the variable name circle is still used
        self.play(circle.animate.shift(LEFT))
        text = Text("Square of side 2", font_size=36)
        text.next_to(circle, RIGHT, buff=0.2)
        self.play(Write(text))
        self.wait(2)

        # Remove the text
        self.play(FadeOut(text))
        self.wait(1)
        self.play(FadeOut(circle))
        self.wait(1)