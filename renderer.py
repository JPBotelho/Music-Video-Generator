from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import os
import os.path

title = "None"
artist = "None"
date = "None"
album = "None"
def main():
    src = "D:/Programas/FFMPEG/bad.mp3"
    output = "D:/Programas/FFMPEG/output.mp4"
    bg = "D:/Programas/FFMPEG/background.jpg"
    font = "\'D:/Programas/FFMPEG/font.ttf\'"
    fontsize = 25
    GetTags(src)    
    
    command = f"ffmpeg -framerate 1 -i \"{bg}\" -i \"{src}\" -filter_complex \"[1:v]scale=600:-1, pad=(16/15)*iw:(16/15)*ih:(ow-iw)/2:(oh-ih)/2:white, [0:v]overlay=(W-w)/7:(H-h)/2:shortest=1,drawtext=fontsize={fontsize}:fontfile={font}:fontcolor=white:text=\'{artist} - {title}\':x=W/2+W/10.5:y=H/11,drawtext=fontsize={fontsize}:fontfile={font}:fontcolor=white:text=\'{album}\':x=W/2+W/10.5:y=2*(H/10),drawtext=fontsize={fontsize}:fontfile={font}:fontcolor=white:text=\'{date}\':x=W/2+W/10.5:y=3*(H/10),format=yuv420p\" -c:v libx264 -r 30 -movflags +faststart \"{output}\""
    os.system(command)

def GetTags(sourcePath):    
    global title
    global artist
    global date
    global album
    fileType = os.path.splitext(sourcePath)[1]
    metadata = None
    if(fileType == ".flac"):
        metadata = FLAC(sourcePath)
    elif (fileType == ".mp3"):
        metadata = EasyID3(sourcePath)
    title = metadata["title"][0]
    artist = metadata["artist"][0]
    date = metadata["date"][0]
    album = metadata["album"][0]
    print("Finished getting tags")
        

if __name__ == '__main__':
    main()