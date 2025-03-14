from manim import *
import random

class QueuingSystem(Scene):
    def construct(self):
        # Create elements
        queue_positions = [LEFT * 4 + RIGHT * 0.25 * i for i in range(5)]  # Queue positions
        system = Rectangle(width=8, height=6, color=YELLOW)  # System box
        system_label = Text("System", font_size=24).next_to(system, UP)
        server = Rectangle(width=1.2, height=1.5, color=BLUE).shift(RIGHT * 2)  # Server box
        server_label = Text("Server", font_size=24).next_to(server, UP)

        # Create customers (dots)
        customers = [Dot(color=GREEN).move_to(pos) for pos in queue_positions]

        # Arrows for entry & exit
        entry_arrow = Arrow(LEFT * 6, queue_positions[0], buff=0.1, color=WHITE)
        exit_arrow = Arrow(server.get_right(), RIGHT * 6, buff=0.1, color=WHITE)

        # Labels for arrival and service rates
        lambda_label = MathTex("\lambda").next_to(entry_arrow, UP)
        mu_label = MathTex("\mu").next_to(server, DOWN)

        # Add elements to scene
        self.play(FadeIn(entry_arrow), FadeIn(exit_arrow), Create(system), Create(server), Write(system_label), Write(server_label), Write(lambda_label), Write(mu_label))
        self.wait(0.5)

        # Animate customers arriving
        for i, customer in enumerate(customers):
            self.play(FadeIn(customer), run_time=0.5)
            self.wait(0.3)

        self.wait(0.5)

        # Customers move through the server one by one
        for i in range(len(customers)):
            wait_time = random.uniform(0.5, 1.5)
            idx = len(customers)-i-1
            self.play(customers[idx].animate.move_to(server.get_left()), run_time=0.5)  # Move to server
            self.wait(0.3)
            self.play(customers[idx].animate.move_to(exit_arrow.get_right()), run_time=wait_time)  # Move to server
            self.wait(0.3)
            self.play(FadeOut(customers[idx]), run_time=0.5)  # Exit the system

        self.wait(1)