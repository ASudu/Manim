from manim import *
import random

class IJEPADemo(Scene):
    def construct(self):
        # STEP 1: Split the image into grid cells
        # Load the image
        image = ImageMobject("media/images/i_jepa/dog_portrait1.jpg").scale(2)

        # Define the number of rows and columns for the grid
        rows, cols = 10, 10

        # Get the width and height of the image
        img_width = image.width
        img_height = image.height

        # Calculate the width and height of each grid cell
        cell_width = img_width / cols
        cell_height = img_height / rows

        # Create a list to hold the grid cells
        grid_cells = []

        # Generate the grid cells
        for i in range(rows):
            row = []
            for j in range(cols):
                # Calculate the position of each cell
                x = -img_width / 2 + (j + 0.5) * cell_width
                y = img_height / 2 - (i + 0.5) * cell_height

                # Create a rectangle for the grid cell
                rect = Rectangle(width=cell_width, height=cell_height)
                rect.move_to([x, y, 0])
                rect.set_stroke(color=BLUE, width=1.5)

                # Add the rectangle to the row list
                row.append(rect)
            grid_cells.append(row)

        # Flatten the grid_cells list for easy manipulation
        grid_cells_flat = [cell for row in grid_cells for cell in row]

        # Choose a random starting cell for the context block
        start_row = random.randint(0, rows - 3)
        start_col = random.randint(0, cols - 3)

        # Define the size of the context block (e.g., 2x2)
        context_block_size = 3

        # Get the adjacent cells to form the context block
        context_block = []
        for i in range(context_block_size):
            for j in range(context_block_size):
                context_block.append(grid_cells[start_row + i][start_col + j])
        
        # Display the image
        self.play(FadeIn(image))
        self.wait(1)

        # Overlay the grid on the image
        self.play(*[Create(cell) for cell in grid_cells_flat])
        self.wait(1)

        # Group the image and grid cells together
        image_and_grid = Group(image, *grid_cells_flat)
        
        # Add the group to the scene
        self.add(image_and_grid)

        # Shrink the image and grid to half their size
        self.play(image_and_grid.animate.scale(0.5))

        # Move the image and grid to the left
        self.play(image_and_grid.animate.shift(LEFT * 3.5))

        # STEP 2: Highlight the context block
        # Highlight the context block
        for cell in context_block:
            cell.set_stroke(color=YELLOW, width=2)
        self.play(*[Transform(cell, cell) for cell in context_block])
        self.wait(0.5)

        # Dim other blocks
        other_blocks = [cell for cell in grid_cells_flat if cell not in context_block]
        self.play(*[cell.animate.set_fill(opacity=0.5) for cell in other_blocks])
        self.wait(0.5)

        # Duplicate the context block
        context_block_copy = Group(*[cell.copy() for cell in context_block])
        self.play(FadeIn(context_block_copy))
        self.wait(0.5)

        # Get the x coordinate of the right edge of the image
        right_edge_x = image.get_right()[1]
        # Move the context block copy to the right
        self.play(context_block_copy.animate.move_to(image.get_right() + RIGHT*0.5))
        self.wait(1)

        # Create a diamond shape for the context encoder
        diamond = Polygon(
            [0, 0.5, 0], [0.5, 0, 0], [0, -0.5, 0], [-0.5, 0, 0],
            color=WHITE, fill_opacity=0.5
        )
        diamond_label = Text("Context Encoder", font_size=16).move_to(diamond.get_bottom() + DOWN*0.1)
        diamond_group = Group(diamond, diamond_label)
        diamond_group.move_to(image.get_right() + RIGHT*2)
        self.play(FadeIn(diamond_group))
        self.wait(1)

        # Draw an arrow from the right edge of the image to the encoder
        arrow1 = always_redraw(lambda: Arrow(
            start=image.get_right(),
            end=diamond.get_left(),
            stroke_width=3,
            color=WHITE,
            buff=0.1
        ))
        self.play(Create(arrow1), context_block_copy.animate.move_to(diamond.get_center()))
        self.wait(0.5)

        # Create an embedding vector
        embedding_vector = Rectangle(width=2, height=0.5, color=GREEN, fill_opacity=0.5)
        embedding_label = Text("Context embedding", font_size=16).move_to(embedding_vector.get_bottom() + DOWN*0.2)
        embedding_group = Group(embedding_vector, embedding_label)
        embedding_group.move_to(diamond_group.get_right() + RIGHT * 2)

        # Draw an arrow from the encoder to the embedding vector
        arrow2 = Arrow(
            start=diamond.get_right(),
            end=embedding_vector.get_left(),
            stroke_width=1.5,
            color=WHITE,
            buff=0.1
        )

        # Move the context block copy out of the diamond as the embedding vector
        self.play(Create(arrow2),Transform(context_block_copy, embedding_group))
        self.wait(0.5)

        # Move the arrows, context encoder, and embedding vector upwards
        self.play(
            arrow1.animate.shift(UP * 2),
            diamond_group.animate.shift(UP * 2),
            arrow2.animate.shift(UP * 2),
            context_block_copy.animate.shift(UP * 2)
        )
        self.wait(1)

        # STEP 3: Highlight the target block
        # Choose a random starting cell for the target block
        target_start_row = random.randint(0, rows - 3)
        target_start_col = random.randint(0, cols - 3)

        # Get the adjacent cells to form the target block
        target_block = []
        for i in range(context_block_size):
            for j in range(context_block_size):
                target_block.append(grid_cells[target_start_row + i][target_start_col + j])

        # Highlight the target block
        for cell in target_block:
            cell.set_stroke(color=RED, width=2)
        self.play(*[Transform(cell, cell) for cell in target_block])
        self.wait(0.5)

        # Dim other blocks
        other_blocks = [cell for cell in grid_cells_flat if cell not in target_block]
        self.play(*[cell.animate.set_fill(opacity=0.5) for cell in other_blocks])
        self.wait(0.5)

        # Duplicate the target block
        target_block_copy = Group(*[cell.copy() for cell in target_block])
        self.play(FadeIn(target_block_copy))
        self.wait(0.5)

        # Move the target block copy to the right
        self.play(target_block_copy.animate.move_to(image.get_right() + RIGHT*0.5))
        self.wait(1)

        # Create a diamond shape for the target encoder
        target_diamond = Polygon(
            [0, 0.5, 0], [0.5, 0, 0], [0, -0.5, 0], [-0.5, 0, 0],
            color=WHITE, fill_opacity=0.5
        )
        target_diamond_label = Text("Target Encoder", font_size=16).move_to(target_diamond.get_bottom() + DOWN*0.1)
        target_diamond_group = Group(target_diamond, target_diamond_label)
        target_diamond_group.move_to(image.get_right() + RIGHT*2)
        self.play(FadeIn(target_diamond_group))
        self.wait(1)

        # Draw an arrow from the right edge of the image to the target encoder
        target_arrow1 = always_redraw(lambda: Arrow(
            start=image.get_right(),
            end=target_diamond.get_left(),
            stroke_width=3,
            color=WHITE,
            buff=0.1
        ))
        self.play(Create(target_arrow1), target_block_copy.animate.move_to(target_diamond.get_center()))
        self.wait(0.5)

        # Create an embedding vector for the target block
        target_embedding_vector = Rectangle(width=2, height=0.5, color=BLUE, fill_opacity=0.5)
        target_embedding_label = Text("Target Embedding", font_size=16).move_to(target_embedding_vector.get_bottom() + DOWN*0.2)
        target_embedding_group = Group(target_embedding_vector, target_embedding_label)
        target_embedding_group.move_to(target_diamond_group.get_right() + RIGHT * 2)

        # Draw an arrow from the target encoder to the target embedding vector
        target_arrow2 = Arrow(
            start=target_diamond.get_right(),
            end=target_embedding_vector.get_left(),
            stroke_width=1.5,
            color=WHITE,
            buff=0.1
        )

        # Move the target block copy out of the target diamond as the target embedding vector
        self.play(Create(target_arrow2),Transform(target_block_copy, target_embedding_group))
        self.wait(0.5)

        # Move the arrows, target encoder, and target embedding vector upwards
        self.play(
            target_arrow1.animate.shift(DOWN * 2),
            target_diamond_group.animate.shift(DOWN * 2),
            target_arrow2.animate.shift(DOWN * 2),
            target_block_copy.animate.shift(DOWN * 2)
        )
        self.wait(1)
