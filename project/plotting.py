from manim import *
import numpy as np

class Graphing(Scene):
    def construct(self):
        # Create axes
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": BLUE},
        ).add_coordinates()

        # Add axes labels
        label = plane.get_axis_labels(x_label="x", y_label="f(x)")

        # Create graph
        func = plane.plot(lambda x: np.sin(x), x_range=[-10, 10], color=WHITE)

        # Label the graph
        func_label = MathTex(r"f(x) = \sin(x)").to_corner(UL).set_color(GREEN)

        # Display graph
        self.play(DrawBorderThenFill(plane))
        self.play(Create(VGroup(label, func, func_label)), run_time=2)
        self.wait()

class secant_grp(Scene):
    def construct(self):
        # Values of x
        k = ValueTracker(-10)

        # Axes
        plane = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": BLUE},
        ).add_coordinates()

        # Add axes labels
        label = plane.get_axis_labels(x_label="x", y_label="f(x)")

        # Graph
        func = plane.plot(lambda x: np.sin(x), x_range=[-10, 10], color=WHITE)

        # Label the graph
        func_label = MathTex(r"f(x) = \sin(x)").to_corner(UL).set_color(GREEN)

        # Sliding secant line
        sec = always_redraw(
            lambda: plane.get_secant_slope_group(k.get_value(), graph=func, dx=0.01, secant_line_color=ORANGE, secant_line_length=3)
        )

        # Display graph
        self.play(DrawBorderThenFill(plane))
        self.play(Create(VGroup(label, func, func_label)), run_time=2)
        self.add(sec)
        self.wait()
        self.play(k.animate.set_value(10), run_time=6)