from moviepy.editor import VideoFileClip, vfx
import cv2
import numpy as np

def apply_cinematic_grade(frame):
    # (Same cinematic grading function as before)
    alpha = 1.15
    beta = -5
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    b, g, r = cv2.split(frame)
    b = cv2.addWeighted(b, .9, np.zeros_like(b), 0, 0)
    r = cv2.addWeighted(r, 1.15, np.zeros_like(r), 0, 0)
    frame = cv2.merge((b, g, r))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.addWeighted(s, 1.15, np.zeros_like(s), 0, 0)
    hsv = cv2.merge((h, s, v))
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return frame

def convert_and_color_grade_with_moviepy(input_path, output_path):
    clip = VideoFileClip(input_path)
    fps = clip.fps

    # Apply color grading to each frame using MoviePy
    def color_grade_frame(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV processing
        graded_frame = apply_cinematic_grade(frame)
        return cv2.cvtColor(graded_frame, cv2.COLOR_BGR2RGB)  # Convert back to RGB for MoviePy

    # Apply the color grading effect to the whole video
    graded_clip = clip.fl_image(color_grade_frame)
    graded_clip.write_videofile(output_path, codec="libx264", fps=fps)

# Run the function
input_video_path = 'c:/VideoEditing/raw_video/London/IMG_3955.mov'
output_video_path = 'c:/VideoEditing/proccessed_video/London/output_video.mp4'
convert_and_color_grade_with_moviepy(input_video_path, output_video_path)
