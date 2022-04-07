import moviepy.editor as mpy
import re



# Set video settings
vcodec = "libx264"
videoquality = "24"
compression = "ultrafast"
fps = 24
threads = 4
method = "compose"

# Global vid end time variable
global vid_end


def complete(name, agent, pin, project, role, scene, duration, edit_name, clip_name, start, end, slate_start, slate_end):
    
    # Generate the text for the slate
    font = 'Ariel'
    color = 'white'

    # name text
    name_text = mpy.TextClip(name, font=font, fontsize=120, color=color)
    name_text = name_text.set_position(('center', 0.3), relative=True)
    name_text = name_text.set_start(0)
    name_text = name_text.set_duration(duration)

    # agent and pin text
    agent_text = mpy.TextClip((f"{agent} - {pin}"), font=font, fontsize=80, color=color)
    agent_text = agent_text.set_position(('center', 0.7), relative=True)
    agent_text = agent_text.set_start(0)
    agent_text = agent_text.set_duration(duration)

    # Check if the user wants the scene text
    if scene is None:
        # project and role text
        project_text = mpy.TextClip((f"{project} - {role}"), font=font, fontsize=100, color=color)
    else:
        # project, role and scene text
        project_text = mpy.TextClip((f"{project} - {role} - {scene}"), font=font, fontsize=100, color=color)
    project_text = project_text.set_position(('center', 0.5), relative=True)
    project_text = project_text.set_start(0)
    project_text = project_text.set_duration(duration)

    # Create the background
    blank_slate = mpy.ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=duration)
        
    # Compose the slate
    slate_clip = mpy.CompositeVideoClip([blank_slate, name_text, project_text, agent_text])
    name_text.close
    agent_text.close
    project_text.close
    blank_slate.close

    # Load clip
    vid = mpy.VideoFileClip(clip_name)

    # Crop the video
    crop = vid.subclip(start, end)
    vid.close

    # Check where the user wants the slate(s) and make the final edit
    fade = -0.4   
    if slate_start is True and slate_end is True:
        edit = mpy.concatenate_videoclips([slate_clip, crop.crossfadein(
            fade), slate_clip.crossfadein(fade)], padding=-fade, method=method)
    elif slate_start is True and slate_end is not True:
        edit = mpy.concatenate_videoclips([slate_clip, crop.crossfadein(fade)], padding=fade, method=method)
    elif slate_start is not True and slate_end is True:
        edit = mpy.concatenate_videoclips([crop, slate_clip.crossfadein(fade)], padding=fade, method=method)
    else:
        edit = crop
    edit.write_videofile(edit_name, threads=threads, fps=fps, codec=vcodec,
                         preset=compression, ffmpeg_params=["-crf", videoquality], logger=None)
    slate_clip.close
    crop.close
    
    return


# Update the global end_vid variable
def set_end(clip_name):
    vid = mpy.VideoFileClip(clip_name)
    global vid_end 
    vid_end = vid.end
    vid.close
    return


# Returns the end time of the video
def get_end():

    # Get the end time of the clip
    end = vid_end

    # Convert the number of seconds to the string used by the crop function
    mins = 0
    while (end - 60) > 0:
        mins = mins + 1
        end = (end - 60)
    end = float(f"{end:,.2f}")

    # Format elements to fit the string needed
    if mins < 10:
        mins = str(f"0{mins}")
    else:
        mins = str(mins)
    
    if end < 10:
        end = str(f"0{end}")
    else:
        end = str(end)

    if len(end[2:]) == 0:
        end = f"{end}.000"
    elif len(end[2:]) == 2:
        end = f"{end}00"
    elif len(end[2:]) == 3:
        end = f"{end}0"

    # Return the formatted string
    return (f"{mins}:{end}")


# Validates whether the times entered by the user are valid
def time_validate(test_start, test_end):

    # Test the users entry has followed the format required
    # Set a format that the users input should've followed
    time_format = re.compile(".{2}:.{2}\..{3}")

    # If the user has entered an invlaid start time
    if not time_format.match(test_start):
        return f"{test_start}"

    # If the user has entered an invlaid end time
    if not time_format.match(test_end):
        return "Invalid end time"

    # Convert the start and end times to ints
    start = int(test_start[:2]) * 60 + int(test_start[3:5]) + float(f"0.{test_start[6:8]}")
    end = int(test_end[:2]) * 60 + int(test_end[3:5]) + float(f"0.{test_end[6:8]}")

    # Check start is greater than 0
    if start < 0:
        return "Start time must be greater than or equal to 0."

    # Check end time is within the video
    if end > vid_end:
        return "End time cannot be after the video has ended."

    # Check it doesn't start before the video ends
    if start >= end:
        return "Start time cannot be after the end time."

    # If all tests pass return true
    return "valid"