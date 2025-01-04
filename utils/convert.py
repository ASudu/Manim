from moviepy.video.io.VideoFileClip import VideoFileClip

def mp4_to_gif(mp4_path, gif_path):
    """Given the file path of a mp4 video, convert it to a gif and save it to the specified path.

    Args:
        mp4_path (str): Path to the mp4 video file.
        gif_path (str): Path to save the gif file.
    """
    clip = VideoFileClip(mp4_path)
    clip.write_gif(gif_path)
    print(f"Successfully converted and saved the gif to {gif_path}")

mp4 = "D:/D_Drive/Github/Manim/project/media/videos/plotting/480p15/secant_grp.mp4"
gif = "D:/D_Drive/Github/Manim/project/media/videos/plotting/480p15/secant_grp.gif"
mp4_to_gif(mp4, gif)