from moviepy.editor import *
from moviepy.video.tools.drawing import circle
from giphy import fetch_gifs
import requests
import os
import random

# Search Giphy
# (optional) convert to argv
search_expression = "godzilla"


rating = 'PG'        # Y, G, PG, PG-13, and R # Y is strictly illustrated content only, ie cartoons.
results = 25

data = fetch_gifs(search_expression, results, rating)    # Y, G, PG, PG-13, and R

W, H = 720, 404     # dimensions of the final video

# resize the clips to the dimensions of the final video

VideoFileClip.reW = lambda clip:  clip.resize(width=W)
VideoFileClip.reH = lambda clip:  clip.resize(height=H)

# title screen

title_clip_tmp = (TextClip(search_expression.title(), font="assets/fonts/Mini_Square.ttf", fontsize=50, color='white'))
title_clip_tmp = (title_clip_tmp.set_pos('center'))


# random colors for the color clip on title
R,G,B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

r_color_clip = (ColorClip(size =(W, H), color=[R,G,B]))

title_clip_w_color = CompositeVideoClip([r_color_clip, title_clip_tmp]).set_duration(3).fadeout(1)

clips = list()  # list to hold video clips from gifs
del_clips = list()

for item in data:

    try:
        url = item['gif_url']
        title = item['title']
        vid_title = title.replace(" ", "_")  # remove white spaces
        del_clips.append(vid_title+'.mp4')  # add extension

        # print(f"processing item = {item}")

        with open('temp.gif', 'wb') as f:
            f.write(requests.get(url).content)

        os.chdir(os.getcwd())
        # Use ffmpeg to convert to get best results
        # brew install ffmpeg   (https://formulae.brew.sh/formula/ffmpeg)
        os.system(f"echo 'y'| ffmpeg -i temp.gif -movflags faststart -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' {vid_title}.mp4 > /dev/null 2>&1")

        v_clip = VideoFileClip(f"{vid_title}.mp4")  # .set_duration(10)
        v_clip_duration = v_clip.duration

        print(f"{title} duration = {v_clip_duration}")

        # final_clip = final_clip.fx(vfx.blackwhite)     # black and white
        final_clip = v_clip.fx(vfx.colorx, 1.25)  # brighten by 1.5 times colorx

        # Append
        clips.append(final_clip)

        # Clean Up
        f.close()
        # os.system(f"echo 'removing {vid_title}.mp4'")
        # os.system(f'rm {vid_title}.mp4')  # removing throws an error

    except:
        print(f"{title} --> errored")
        pass


clips_combined = concatenate_videoclips(clips, method='compose')
d = clips_combined.duration
t = time_quotient = d // 4
t_2 = t*2
t_3 = t*3
# print(f"d = {d} t = {t} t_2 = {t_2} t_3 = {t_3}")

title_vid_top_right_tmp = clips_combined.subclip(0, t)  # 0, t is blank
title_vid_top_left_tmp = clips_combined.subclip(t, t_2)
title_vid_bottom_right_tmp = clips_combined.subclip(t_2,t_3)
title_vid_bottom_left_tmp = clips_combined.subclip(t_3, d)

title_vid_top_right = (title_vid_top_right_tmp.
         resize((W/3,H/3)).    # one third of the total screen
         margin(2,color=(255,255,255)).  # white margin
         margin(top=10, right=10, opacity=0). # transparent
         set_pos(('right','top')).set_duration(3))

title_vid_top_left = (title_vid_top_left_tmp.
         resize((W/3,H/3)).    # one third of the total screen
         margin(2,color=(255,255,255)).  #  white margin
         margin(top=10, left=10, opacity=0). # transparent
         set_pos(('left','top')).set_duration(3))

title_vid_bottom_right = (title_vid_bottom_right_tmp.
         resize((W/3,H/3)).    # one third of the total screen
         margin(2,color=(255,255,255)).  #  white margin
         margin(bottom=10, right=10, opacity=0). # transparent
         set_pos(('right','bottom')).set_duration(3))

title_vid_bottom_left = (title_vid_bottom_left_tmp.
         resize((W/3,H/3)).    # one third of the total screen
         margin(2,color=(255,255,255)).  #  white margin
         margin(bottom=10, left=10, opacity=0). # transparent
         set_pos(('left','bottom')).set_duration(3))


# Create title clip with 4 subclips

title_clip = CompositeVideoClip([title_clip_w_color,
                                 title_vid_bottom_right,
                                 title_vid_top_right,
                                 title_vid_bottom_left,
                                 title_vid_top_left]).set_duration(3).fadeout(0.5)

## Credits

credits_text = f"""
CREDITS

Title: {search_expression.title()}

Music by Titan0346
https://soundcloud.com/shaurya-m

"""

# credits
the_end = (TextClip(credits_text,
                    fontsize=30, interline=15, bg_color='black', font="assets/fonts/Mini_Square.ttf",
                    size=(W, H), color='white').set_pos(('center', 'center')).set_duration(4).fadein(0.5))

# Main sequence
main_vid = concatenate([title_clip, clips_combined, the_end], method='compose')

main_vid.add_mask()

# The mask is a circle with vanishing radius r(t) = 800-200*t
main_vid.mask.get_frame = lambda t: circle(screensize=(W,H),
                                       center=(W/2, H/4),
                                       radius=max(0,int(800-200*t)),
                                       col1=1, col2=0, blur=4)

# pick a random audio clip from a list of clips

audio_clips = ['assets/music/m0.mp3', 'assets/music/titan0346_8bit_invaders.wav', 'assets/music/titan0346_cyberpunk.wav']

r_audio_id = random.randint(0, len(audio_clips)-1)
r_audio_clip = audio_clips[r_audio_id]
print(f"audio clip in use = {r_audio_clip}")

music_loop = afx.audio_loop(AudioFileClip(r_audio_clip).fx(afx.volumex, 0.2), duration=int(main_vid.duration))

# music_loop.preview()  # works

video_with_audio = main_vid.set_audio(music_loop)


filename_prefix = []

filename_suffix = [' compilation', ' collection', ' catalog']




# video_with_audio.preview()
try:

    video_with_audio.write_videofile(f"out/{search_expression}.mp4", fps=25, bitrate="10000k", audio_bitrate='1000k',
                                 audio=True,
                                 codec='libx264',          # libx264, mpeg4
                                 audio_codec='aac',
                                 temp_audiofile='temp-audio.m4a',
                                 remove_temp=True,
                                 # logger=None,
                                 threads=4)     # for performance boost
except:
    # delete tmp clips in case of error making vid
    for item in del_clips:
        os.system(f"echo 'removing {item}'")
        os.system(f"rm {item}")

# Cleanup
for item in del_clips:
    os.system(f"echo 'removing {item}'")
    os.system(f"rm {item}")
