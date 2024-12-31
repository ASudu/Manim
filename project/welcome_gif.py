from manim import *

class WelcomeGitHub(Scene):
    def construct(self):
        # Grid background
        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        self.add(plane)

        # Glowing "Welcome" text
        welcome_text = Text("Welcome", font_size=96, gradient=(BLUE, PURPLE))
        glowing_welcome = welcome_text.copy().set_color(YELLOW).set_opacity(0.4)

        # Secondary text
        repo_text = Text("to my GitHub Repo!", font_size=48, color=WHITE)
        repo_text.next_to(welcome_text, DOWN, buff=0.5)

        # Show grid and create welcome text
        self.play(FadeIn(plane, run_time=2))
        self.play(Write(welcome_text))

        # Simulate glow with fading opacity
        for _ in range(2):  # Repeat glowing effect
            self.add(glowing_welcome)
            self.play(glowing_welcome.animate.set_opacity(0.8), run_time=0.5)
            self.play(glowing_welcome.animate.set_opacity(0.4), run_time=0.5)
        self.remove(glowing_welcome)

        # Slide in secondary text
        self.play(Write(repo_text))
        self.wait(1)

        # Pulsing effect at the end
        self.play(
            welcome_text.animate.scale(1.2).set_color(YELLOW),
            repo_text.animate.set_color(GREEN).scale(0.9),
            run_time=1.5,
        )
        self.wait(2)

class WelcomeGraphAnimation(Scene):
    def construct(self):
        # Grid background
        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        self.play(FadeIn(plane))

        # Glowing "Welcome" text
        welcome_text = Text("Welcome", font_size=96, gradient=(BLUE, PURPLE))
        glowing_welcome = welcome_text.copy().set_color(YELLOW).set_opacity(0.4)
        
        # Create axes
        head = Circle(radius=0.5, color=WHITE).shift(UP * 2)
        body = Line(head.get_bottom(), head.get_bottom() + DOWN * 2, color=WHITE)
        left_arm = Line(body.get_start() + LEFT * 0.5, body.get_start() + LEFT * 2, color=WHITE)
        right_arm = Line(body.get_start() + RIGHT * 0.5, body.get_start() + RIGHT * 2, color=WHITE)
        left_leg = Line(body.get_end(), body.get_end() + LEFT * 1 + DOWN * 2, color=WHITE)
        right_leg = Line(body.get_end(), body.get_end() + RIGHT * 1 + DOWN * 2, color=WHITE)

        # Group the stick figure
        stick_figure = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)

        # Initial appearance
        self.play(FadeIn(stick_figure))
        self.wait(1)

        # Move stick figure to the left
        self.play(stick_figure.animate.shift(LEFT * 4),Write(welcome_text),run_time=2)
        self.wait(1)

        # Define dance moves
        def dance_move_1():
            return [
                left_arm.animate.rotate(PI / 4, about_point=body.get_start()),
                right_arm.animate.rotate(-PI / 4, about_point=body.get_start()),
                left_leg.animate.rotate(-PI / 6, about_point=body.get_end()),
                right_leg.animate.rotate(PI / 6, about_point=body.get_end()),
            ]

        def dance_move_2():
            return [
                left_arm.animate.rotate(-PI / 4, about_point=body.get_start()),
                right_arm.animate.rotate(PI / 4, about_point=body.get_start()),
                left_leg.animate.rotate(PI / 6, about_point=body.get_end()),
                right_leg.animate.rotate(-PI / 6, about_point=body.get_end()),
            ]

        # Perform the dance moves repeatedly
        for _ in range(3):
            self.add(glowing_welcome)
            self.play(*dance_move_1(),glowing_welcome.animate.set_opacity(0.8), run_time=0.5)
            self.play(*dance_move_2(),glowing_welcome.animate.set_opacity(0.4), run_time=0.5)
        self.remove(glowing_welcome)

        # Add a final pose
        final_pose = [
            left_arm.animate.rotate(-PI / 3, about_point=body.get_start()),
            right_arm.animate.rotate(PI / 3, about_point=body.get_start()),
            left_leg.animate.rotate(-PI / 3, about_point=body.get_end()),
            right_leg.animate.rotate(PI / 3, about_point=body.get_end()),
        ]
        self.play(*final_pose, run_time=1)

        # End the animation
        self.wait(2)