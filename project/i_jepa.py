from manim import *
import random

class IJEPADemo(Scene):
    def construct(self):
        # STEP 1: Split the image into grid cells
        # Load the image
        image = ImageMobject("media/images/i_jepa/dog_portrait1.jpg").scale(2)
        num_examples = 2
        colors = [RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, MAROON]

        # Define the number of rows and columns for the grid
        rows, cols = 4, 4

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

        # Define the size of the context block (e.g., 2x2)
        context_width = 2
        context_height = 3

        # Choose a random starting cell for the context block
        start_row = random.randint(0, rows - context_height)
        start_col = random.randint(0, cols - context_width)

        # Get the adjacent cells to form the context block
        context_block = []
        for i in range(context_height):
            for j in range(context_width):
                context_block.append(grid_cells[start_row + i][start_col + j])
        
        # Display the image
        self.play(FadeIn(image))
        self.wait(1)

        step1_text = Text("Step 1: Split the image into grid cells", font_size=24).to_edge(DOWN)

        # Overlay the grid on the image
        self.play(*[Create(cell) for cell in grid_cells_flat], Write(step1_text))
        self.wait(1)

        # Group the image and grid cells together
        image_and_grid = Group(image, *grid_cells_flat)
        
        # Add the group to the scene
        self.add(image_and_grid)

        # Shrink the image and grid to half their size
        self.play(image_and_grid.animate.scale(0.5), FadeOut(step1_text))

        # Move the image and grid to the left
        self.play(image_and_grid.animate.shift(LEFT * 3.5))

        # Repeat the process for each example
        for p in range(num_examples):
            # STEP 2: Highlight the context block
            step2_text = Text("Step 2: Select the context block and mask the rest of the image", font_size=24).to_edge(DOWN)
            # Highlight the context block
            for cell in context_block:
                cell.set_stroke(color=YELLOW, width=2)
            self.play(*[Transform(cell, cell) for cell in context_block], Write(step2_text))
            self.wait(0.5)

            # Dim other blocks
            other_blocks = [cell for cell in grid_cells_flat if cell not in context_block]
            self.play(*[cell.animate.set_fill(opacity=0.5) for cell in other_blocks])
            self.wait(0.5)

            # Duplicate the context block
            context_block_copy = Group(*[cell.copy() for cell in context_block])
            self.play(FadeIn(context_block_copy))
            self.wait(0.5)

            # Move the context block copy to the right
            self.play(context_block_copy.animate.move_to(image.get_right() + RIGHT*0.5), FadeOut(step2_text))
            self.wait(1)

            # STEP 3: Encode the context block
            step3_text = Text("Step 3: Encode the context block", font_size=24).to_edge(DOWN)

            # Create a diamond shape for the context encoder
            c_enc = Polygon(
                [0, 0.5, 0], [0.5, 0, 0], [0.5, -0.5, 0], [0, -1.0, 0],
                color=WHITE, fill_opacity=0.5
            )
            c_enc_label = Text("Context Encoder (ViT)", font_size=16).move_to(c_enc.get_bottom() + DOWN*0.1)
            c_enc_eq = MathTex(r"f_{\theta}").scale(0.5).move_to(c_enc.get_center() + UP*0.1)
            c_enc_group = Group(c_enc, c_enc_label, c_enc_eq)
            c_enc_group.move_to(image.get_right() + RIGHT*2)
            self.play(FadeIn(c_enc_group))
            self.wait(1)

            # Draw an arrow from the right edge of the image to the encoder
            c_arrow1 = always_redraw(lambda: Arrow(
                start=image.get_right(),
                end=c_enc.get_left(),
                stroke_width=3,
                color=WHITE,
                buff=0.1
            ))
            self.play(Create(c_arrow1), context_block_copy.animate.move_to(c_enc.get_center()), Write(step3_text))
            self.wait(0.5)

            # Create an embedding vector
            c_emb_vector = Rectangle(width=2, height=0.5, color=YELLOW, fill_opacity=0.5)
            c_emb_label = Text("Context embedding", font_size=16).move_to(c_emb_vector.get_bottom() + DOWN*0.2)
            c_emb_group = Group(c_emb_vector, c_emb_label)
            c_emb_group.move_to(c_enc_group.get_right() + RIGHT * 2)

            # Draw an arrow from the encoder to the embedding vector
            c_arrow2 = Arrow(
                start=c_enc.get_right(),
                end=c_emb_vector.get_left(),
                stroke_width=1.5,
                color=WHITE,
                buff=0.1
            )

            # Move the context block copy out of the diamond as the embedding vector
            self.play(Create(c_arrow2),Transform(context_block_copy, c_emb_group))
            self.wait(0.5)

            # Move the arrows, context encoder, and embedding vector upwards
            self.play(
                c_arrow1.animate.shift(UP * 2),
                c_enc_group.animate.shift(UP * 2),
                c_arrow2.animate.shift(UP * 2),
                context_block_copy.animate.shift(UP * 2),
                FadeOut(step3_text)
            )
            self.wait(1)

            # STEP 4: Highlight the target block
            step4_text = Text("Step 4: Select the target block from the original unmasked image", font_size=24).to_edge(DOWN)

            # Define the size of the target block (e.g., 2x2)
            target_width = 2
            target_height = 2

            # Choose a random starting cell for the target block
            target_start_row = random.randint(0, rows - target_height)
            target_start_col = random.randint(0, cols - target_width)

            # Get the adjacent cells to form the target block
            target_block = []
            for i in range(target_height):
                for j in range(target_width):
                    target_block.append(grid_cells[target_start_row + i][target_start_col + j])

            # Highlight the target block
            self.play(*[cell.animate.set_fill(opacity=0) for cell in grid_cells_flat])
            for cell in target_block:
                cell.set_stroke(color=colors[p%len(colors)], width=2)
            self.play(*[Transform(cell, cell) for cell in target_block], Write(step4_text))
            self.wait(0.5)

            # Dim other blocks
            other_blocks = [cell for cell in grid_cells_flat if cell not in target_block and cell not in context_block]
            self.play(*[cell.animate.set_fill(opacity=0.5) for cell in other_blocks])
            self.wait(0.5)

            # Duplicate the target block
            target_block_copy = Group(*[cell.copy() for cell in target_block])
            self.play(FadeIn(target_block_copy))
            self.wait(0.5)

            # Move the target block copy to the right
            self.play(target_block_copy.animate.move_to(image.get_right() + RIGHT*0.5))
            self.wait(1)

            # STEP 5: Encode the target block
            step5_text = Text("Step 5: Encode the target block", font_size=24).to_edge(DOWN)
            # Create a diamond shape for the target encoder
            t_enc = Polygon(
                [0, 0.5, 0], [0.5, 0, 0], [0.5, -0.5, 0], [0, -1.0, 0],
                color=WHITE, fill_opacity=0.5
            )
            t_enc_label = Text("Target Encoder (ViT)", font_size=16).move_to(t_enc.get_bottom() + DOWN*0.1)
            t_enc_eq = MathTex(r"f_{\tilde{\theta}}").scale(0.5).move_to(t_enc.get_center() + UP*0.1)
            t_enc_group = Group(t_enc, t_enc_label, t_enc_eq)
            t_enc_group.move_to(image.get_right() + RIGHT*2)
            self.play(FadeIn(t_enc_group), FadeOut(step4_text))
            self.wait(1)

            # Draw an arrow from the right edge of the image to the target encoder
            t_arrow1 = always_redraw(lambda: Arrow(
                start=image.get_right(),
                end=t_enc.get_left(),
                stroke_width=3,
                color=WHITE,
                buff=0.1
            ))
            self.play(Create(t_arrow1), target_block_copy.animate.move_to(t_enc.get_center()), Write(step5_text))
            self.wait(0.5)

            # Create an embedding vector for the target block
            t_emb_vector = Rectangle(width=2, height=0.5, color=colors[p%len(colors)], fill_opacity=0.5)
            t_emb_label = Text("Target Embedding", font_size=16).move_to(t_emb_vector.get_bottom() + DOWN*0.2)
            t_emb_group = Group(t_emb_vector, t_emb_label)
            t_emb_group.move_to(t_enc_group.get_right() + RIGHT * 2)

            # Draw an arrow from the target encoder to the target embedding vector
            t_arrow2 = Arrow(
                start=t_enc.get_right(),
                end=t_emb_vector.get_left(),
                stroke_width=1.5,
                color=WHITE,
                buff=0.1
            )

            # Move the target block copy out of the target diamond as the target embedding vector
            self.play(Create(t_arrow2),Transform(target_block_copy, t_emb_group))
            self.wait(0.5)

            # Move the arrows, target encoder, and target embedding vector upwards
            self.play(
                t_arrow1.animate.shift(DOWN * 2),
                t_enc_group.animate.shift(DOWN * 2),
                t_arrow2.animate.shift(DOWN * 2),
                target_block_copy.animate.shift(DOWN * 2),
                FadeOut(step5_text)
            )
            self.wait(1)

            # Fade out everything except image, grid and the embeddings
            self.play(
                FadeOut(c_arrow1),
                FadeOut(c_arrow2),
                FadeOut(t_arrow1),
                FadeOut(t_arrow2),
                FadeOut(c_enc_group),
                FadeOut(t_enc_group)
            )
            self.wait()

            # Move the embeddings close to the image
            self.play(context_block_copy.animate.shift(LEFT*3.5), target_block_copy.animate.shift(LEFT*3.5))
            self.wait()

            # STEP 6: Input context embedding and position embedding to the predictor
            step6_text = Text("Step 6: Input context embedding and position embedding to the predictor", font_size=24).to_edge(DOWN)

            # Positional information
            target_copy = Group(*[cell.copy() for cell in target_block])
            context_copy = Group(*[cell.copy() for cell in context_block])
            highlighted = Group(target_copy, context_copy)
            self.play(highlighted.animate.move_to(context_block_copy.get_right() + RIGHT*0.8))
            pos_text = Text("Position Encoding", font_size=16).move_to(highlighted.get_top() + UP*0.2)
            pos_info = Group(highlighted, pos_text)
            pred_in = Group(context_block_copy, pos_info)

            # Move the group to the left to make more space for the predictor
            self.play(image_and_grid.animate.shift(LEFT), pred_in.animate.shift(LEFT*2), target_block_copy.animate.shift(LEFT*2))

            # Create a diamond shape for the predictor
            pred = Polygon(
                [0, 0.5, 0], [0.5, 0, 0], [0.5, -0.5, 0], [0, -1.0, 0],
                color=WHITE, fill_opacity=0.5
            )
            pred_label = Text("Predictor (Narrow ViT)", font_size=16).move_to(pred.get_bottom() + DOWN*0.1)
            pred_eq = MathTex(r"g_{\phi}").scale(0.5).move_to(pred.get_center() + UP*0.1)
            pred_group = Group(pred, pred_label, pred_eq)
            pred_group.move_to(pred_in.get_right() + RIGHT)
            self.play(FadeIn(pred_group), FadeOut(step5_text))
            self.wait(1)

            # Draw an arrow to show direction of input
            pred_arrow1 = Arrow(
                start=context_block_copy.get_right(),
                end=pred.get_left(),
                stroke_width=3,
                color=WHITE,
                buff=0.1
            )
            self.play(pred_in.animate.scale(0.25))
            self.play(Create(pred_arrow1), pred_in.animate.move_to(pred.get_center()), Write(step6_text))
            self.wait(0.5)

            # Create an embedding vector for the target block
            t_pred_vector = Rectangle(width=2, height=0.5, color=BLUE, fill_opacity=0.5)
            t_pred_label = Text("Predicted Target Embedding", font_size=16).move_to(t_pred_vector.get_bottom() + DOWN*0.2)
            t_pred_group = Group(t_pred_vector, t_pred_label)
            t_pred_group.move_to(pred_group.get_right() + RIGHT*2)

            # Draw an arrow from the target encoder to the target embedding vector
            pred_arrow2 = Arrow(
                start=pred.get_right(),
                end=t_pred_vector.get_left(),
                stroke_width=1.5,
                color=WHITE,
                buff=0.1
            )

            # Move the target block copy out of the target diamond as the target embedding vector
            self.play(Create(pred_arrow2), Transform(pred_in, t_pred_group))
            self.wait(1)
            self.play(FadeOut(pred_group), FadeOut(pred_arrow1), FadeOut(pred_arrow2))
            self.play(pred_in.animate.move_to(target_block_copy.get_top() + UP*5))

            # STEP 7: Compute the loss
            step7_text = Text("Step 7: Compute the loss", font_size=24).to_edge(DOWN)
            loss_box = Rectangle(width=2, height=0.5, color=GREEN, fill_opacity=0.5)
            loss_text = Text("L2 Loss", font_size=16).move_to(loss_box.get_center())
            loss_group = Group(loss_box, loss_text)
            loss_group.move_to(image_and_grid.get_right() + RIGHT*2)
            self.play(FadeIn(loss_group), FadeOut(step6_text))
            self.wait(1)

            # Scale them before putting through Loss box
            self.play(target_block_copy.animate.scale(0.5), pred_in.animate.scale(0.5), Write(step7_text))
            start1, end1 = pred_in.get_bottom(), loss_box.get_top()
            start2, end2 = target_block_copy.get_top(), loss_box.get_bottom()

            # Draw an arrow from the predictor to the loss
            loss_arrow1 = Arrow(
                start=start1,
                end=end1,
                stroke_width=3,
                color=WHITE,
                buff=0.1
            )

            loss_arrow2 = Arrow(    
                start=start2,
                end=end2,
                stroke_width=3,
                color=WHITE,
                buff=0.1
            )
            self.wait(1)
            self.play(target_block_copy.animate.move_to(loss_group.get_center() + UP*0.1), Create(loss_arrow2),
                      pred_in.animate.move_to(loss_group.get_center() + DOWN*0.1), Create(loss_arrow1))
            self.wait(1)
            loss_vec = Group(target_block_copy, pred_in)

            # L2 norm equation
            eq = MathTex(
                r"\|",  # Opening norm bar
                r"x",  # True target
                r"-",  # Minus sign
                r"x",  # Pred target
                r"\|_2"  # L2 norm
            ).scale(1.5).to_edge(UP)

            # Coloring the equation components to match the vectors
            eq[1].set_color(BLACK) 
            eq[3].set_color(BLACK)

            # Small rectangles (representing vectors in the equation)
            small_vec1 = Rectangle(width=0.5,height=0.1, color=colors[p%len(colors)], fill_opacity=0.5).next_to(eq[3], ORIGIN, buff=0.1)
            small_vec2 = Rectangle(width=0.5,height=0.1, color=BLUE, fill_opacity=0.5).next_to(eq[1], ORIGIN, buff=0.1)
            loss_eq_grp = Group(eq, small_vec1, small_vec2)
            loss_eq_grp.move_to(loss_group.get_right() + RIGHT*2)

            # Arrow from loss box to equation
            loss_arrow3 = Arrow(
                start=loss_group.get_right(),
                end=loss_eq_grp.get_left(),
                stroke_width=3,
                color=WHITE,
                buff=0.1
            )

            self.play(FadeOut(loss_arrow1), FadeOut(loss_arrow2))
            self.wait(1)
            self.play(Create(loss_arrow3), Transform(loss_vec, loss_eq_grp))
            self.wait(1)
            # Fade out all objects except the image, grid, and the context and target block
            self.play(FadeOut(Group(*[mobj for mobj in self.mobjects if mobj not in [image_and_grid, *grid_cells_flat, context_block_copy, target_block_copy]])))
            self.wait(2)


