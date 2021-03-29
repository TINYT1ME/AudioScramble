from os import remove, devnull
from sys import __stdout__
import time
from moviepy.editor import *
from colorama import Fore

from math import ceil

# Defining Variables
AUDIO = AudioFileClip("10sec.mp3")  # Source audio file
TEMP = "temp_output"  # Temp audio files(deleted when done)
OUTPUT = "Testencrypted.mp3"  # Final audio file(output)
DURATION = AUDIO.duration  # Duration of original audio file
PARTS = 100  # Max PARTS per clip(the higher the harder to understand while encrypted)
MAX = 190  # MAX recursion(10 == 1s)DONT CHANGE
TIMES = int(ceil(AUDIO.duration * PARTS / MAX))  # How many temp clips to make
num = "654734732470203321730987128371892379081723891273908712893712980371902837981203719082371980237918027390812730981273891729805473208957098237529803758904375283947589037542890752389457328947532489752903847532895473209845723089457230985472398054723908457234895723089475298037532809752308947509283475289304573208957329085732490857239804572340985723094857238940572398045723980457239804752389457239845723489572390845723498057239804572348957230984759082347530298578094573208957230985474890574283945708923405787342509329875492834753920857239850748932057982345"  # Encryption key
clips = []  # Array used to scramble clips
recursive_clip = AUDIO.subclip(0, 0)  # Each recursive_clip will end up as TEMP
final_clip = AUDIO.subclip(0, 0)  # End up as OUTPUT
recursion_counter = 0  # Used to count recursions
timer = time.process_time()  # Start timer to find out how long code takes
value_error = False  # Only written in because i suck at python


# Function used to sort 2d array by second entry
def sort_second(val):
    return val[1]


# Disable print(for imports)
def block_print():
    sys.stdout = open(devnull, 'w')


# Restore print(for imports)
def enable_print():
    sys.stdout = __stdout__


block_print()


# For printing a pretty message
def printing(message):
    enable_print()
    print(f"\nENCRYPTOR #> {message}")
    block_print()


printing(f"Total parts: {TIMES}")

# Scramble audio into array
for i in range(1, int(DURATION * PARTS)):
    num_index = i % len(num)
    clips.append([i / PARTS, (i * int(num[int(num_index) - 1])) / PARTS])
#printing(clips)
clips.sort(key=sort_second)

# Compiles each MAX into TEMP
for i in range(0, TIMES):
    recursive_clip = AUDIO.subclip(0, 0)
    printing(Fore.YELLOW + f"{i + 1}/{TIMES}" + Fore.RESET)
    for x in range(0 + MAX * i, MAX + MAX * i):
        recursion_counter += 1
        if recursion_counter % MAX == 0:
            clip = AUDIO.subclip(clips[x][0], clips[x][0] + 1 / PARTS)
            recursive_clip = concatenate_audioclips([recursive_clip, clip])
            break
        try:
            #printing(f"{clips[x][0]}, {clips[x][0] + 1 / PARTS}")
            clip = AUDIO.subclip(clips[x][0], clips[x][0] + 1 / PARTS)
            recursive_clip = concatenate_audioclips([recursive_clip, clip])
        except IndexError:
            break
    try:
        part_clip = concatenate_audioclips([recursive_clip])
        part_clip.write_audiofile(f"{TEMP}{i}.mp3")
    except ValueError:
        value_error = True
        TIMES -= 1
        break

if value_error:
    remove(f"{TEMP}{TIMES}.mp3")

# Compiles all TEMP into OUTPUT clip
for i in range(TIMES):
    target_clip = AudioFileClip(f"{TEMP}{i}.mp3")
    final_clip = concatenate_audioclips([final_clip, target_clip])

# Outputting encrypted file
final_clip.write_audiofile(OUTPUT)

# CLEAN UP
for i in range(TIMES):
    remove(f"{TEMP}{i}.mp3")
    printing(Fore.LIGHTMAGENTA_EX + f"Removed: {TEMP}{i}.mp3" + Fore.RESET)

printing(Fore.BLUE + f"Original length: {AUDIO.duration}" + Fore.RESET)
printing(Fore.BLUE + f"Encrypted length: {AudioFileClip(OUTPUT).duration}" + Fore.RESET)
printing(Fore.BLUE + f"Time Taken: {time.process_time() - timer}" + Fore.RESET)
printing(Fore.MAGENTA + "Finished :-)")
