from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import os.path
from pathlib import Path

# ffmpeg -framerate 1 -i "background.jpg" -i test.flac -i pain.flac -i gold.flac -filter_complex "[1:v]scale=600:-1[ovrl]; [0:v][ovrl]overlay=(W-w)/7:(H-h)/2; [1:a][2:a][3:a]concat=n=3:v=0:a=1" -c:v libx264 -r 30 -movflags +faststart "newout.mp4"
#'ffmpeg -framerate 1 -i "background.jpg" -i "D:\\Programas\\FFMPEG\\Album\\01 - Smoking.flac" -i "D:\\Programas\\FFMPEG\\Album\\02 - 1st Thing First.flac" -i "D:\\Programas\\FFMPEG\\Album\\03 - Two Gats Up.flac" -i "D:\\Programas\\FFMPEG\\Album\\04 - Blow Up.flac" -i "D:\\Programas\\FFMPEG\\Album\\05 - Party People.flac" -i "D:\\Programas\\FFMPEG\\Album\\06 - If You Only Knew.flac" -i "D:\\Programas\\FFMPEG\\Album\\07 - Hit Me With That Shit.flac" -i "D:\\Programas\\FFMPEG\\Album\\08 - Hip Hop.flac" -i "D:\\Programas\\FFMPEG\\Album\\09 - Chamber Danger.flac" -i "D:\\Programas\\FFMPEG\\Album\\10 - Underground Emperor.flac" -i "D:\\Programas\\FFMPEG\\Album\\11 - Life Bid.flac" -i "D:\\Programas\\FFMPEG\\Album\\12 - Don't Go Against the Grain.flac" -i "D:\\Programas\\FFMPEG\\Album\\13 - Things Ain't What They Used To Be.flac" -i "D:\\Programas\\FFMPEG\\Album\\14 - Black On Black Crime.flac" -filter_complex "[1:v]scale=600:-1[ovrl]; [0:v][ovrl]overlay=(W-w)/7:(H-h)/2; [1:a][2:a][3:a][4:a][5:a][6:a][7:a][8:a][9:a][10:a][11:a][12:a][13:a][14:a]concat=n=14:v=0:a=1" -c:v libx264 -r 30 -movflags +faststart "albumVideo.mp4"'
def main():
    videoOutput = "BlackMarketMilitia.mp4"
    path = "D:/Downloads/Music/Collection/Black Market Militia/Black Market Militia (2005) - Black Market Militia"
    backgroundPath = "D:/Programas/FFMPEG/background.jpg"
    font = "\'D:/Programas/FFMPEG/font.ttf\'"
    fontsize = 25
    
    q = Path(path)
    if not(q.exists()):
        raise Exception("Directory does not exist.")
    if not(q.is_dir()):
        raise Exception("String is not valid directory.")

    files = list(q.glob('*.flac'))    

    if (len(files)==0):
        files = list(q.glob("*.mp3"))
        if(len(files)==0):
            raise Exception("Directory has no .flac or .mp3 files.")
        else:
            metadata = EasyID3(files[0])
    else:
        metadata = FLAC(files[0])
    
    try:
        album = metadata["album"][0]
    except:
        raise Exception("File #0 does not have \'album\' tag")
    # Remove invalid characters (commas and single-quotes)
    album = album.replace("\'", "")
    album = album.replace(",", "")
    
    try:
        artist = metadata["artist"][0]
    except:
        raise Exception("File #0 does not have \'artist\' tag")
      
    try:
        date = metadata["date"][0]
    except:
        try:
            date = metadata["year"][0]
        except:
            raise Exception("File #0 does not have \'date\' nor \'year\' tags")
    
    #album = album.replace("\"", "")
    length = 0

    try:
        for file in files:
            length += FLAC(file).info.length
    except:
        for file in files:
            length += MP3(file).info.length

    command = f"ffmpeg -loop 1 -framerate 1 -i \"{backgroundPath}\" "
    for flacFile in files:
        command += (f"-i \"{flacFile}\" ")
            
        
    command += f"-filter_complex \"[1:v]scale=600:-1[ovrl]; [0:V]drawtext=fontsize=25:fontfile=\"D:/Programas/FFMPEG/font.ttf\":fontcolor=white:text={artist}:x=W/2+W/10.5:y=H/11[f1], [f1]drawtext=fontsize=25:fontfile=\"D:/Programas/FFMPEG/font.ttf\":fontcolor=white:text={album}:x=W/2+W/10.5:y=2*(H/10)[f2],[f2]drawtext=fontsize=25:fontfile=\"D:/Programas/FFMPEG/font.ttf\":fontcolor=white:text={date}:x=W/2+W/10.5:y=3*(H/10)[bg]; [bg][ovrl]overlay=(W-w)/7:(H-h)/2; "
    for i in range(len(files)):
        z = i+1
        command += f"[{z}:a]"
    fileCount = len(files)
    command += f"concat=n={fileCount}:v=0:a=1[final]\" -map 0:v -map [final]:a -t {length} -r 1 -movflags +faststart \"{videoOutput}\""
    print(command)
    os.system(command)

if __name__ == '__main__':
    main()