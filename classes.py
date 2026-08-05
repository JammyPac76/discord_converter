from pathlib import Path
import cv2
from functions import assign_codec

class VideoFile:
    def __init__(self, filepath, imported_file=None):
        self.filepath = Path(filepath)
        self.filename = self.filepath.stem
        self.fileformat = self.filepath.suffix
        self.video_codec, self.audio_codec = assign_codec(self.fileformat)

        #Get more in-depth data within the video
        if self.filepath.exists() and not imported_file:
            video = cv2.VideoCapture(self.filepath)
            self.fps = video.get(cv2.CAP_PROP_FPS)
            self.frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
            self.duration = self.frame_count/self.fps   #In seconds!
            self.width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
            video.release()
