import cv2
from src.types import Frame

class VideoIO:
    fps =30.
    def read(self, src:'str | int'):
        frames:list[Frame] =[]
        video =cv2.VideoCapture(src)
        if video.isOpened(): self.fps =video.get(cv2.CAP_PROP_FPS)
        print("[+] Loading video")
        while video.isOpened():
            okay, frame =video.read()
            if not okay: break
            frames.append(frame)
        video.release()
        return frames
    
    def write(self, frames:list[Frame], out:str, fps =None, fourcc ='mp4v'):
        if not len(frames): return
        fps =fps if fps else self.fps
        fourcc =cv2.VideoWriter_fourcc(*fourcc)
        height, width, *_ =frames[0].shape
        video =cv2.VideoWriter(out, fourcc, fps, (width, height))
        print("[+] Writing video")
        for frame in frames: video.write(frame)
        video.release()
    
    def save_frames(self, frames, outDir:str):
        print("[+] Saving frames")
        count =0
        for i in range(0, len(frames), int(self.fps)):
            cv2.imwrite(f"{outDir}/{count if count>9 else '0' +str(count)}.png", frames[i])
            count +=1