import subprocess
import os
from datetime import datetime
import psutil
import pygame
import sys


def get_open_programs():
    open_programs = []
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_name = process.info['name']
            open_programs.append(process_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return open_programs


if __name__ == "__main__":
    open_programs = get_open_programs()
    for program in open_programs:
        print(program)
    print(len(open_programs))
    if 'Count Time.exe' in open_programs:
        pygame.init()
        X = 300
        Y = 150
        display_surface = pygame.display.set_mode((X, Y))
        pygame.display.set_caption('The program is running.')
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render('The program is running.', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        clock = pygame.time.Clock()
        t1 = datetime.now()
        while True:
            if (datetime.now() - t1).total_seconds() > 5:
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()

            display_surface.fill((255, 255, 255))
            display_surface.blit(text, textRect)
            pygame.display.flip()
            clock.tick(60)


    else:
        # venv_activate_script = os.path.join('.venv', 'Scripts', 'activate.bat')
        # script1 = 'program_icon.py'
        # script2 = 'Count Time.py'
        #
        # # Create a temporary batch script
        # batch_script_content = f'call "{venv_activate_script}" && python "{script1}"'
        # with open('temp_batch_script1.bat', 'w') as batch_script_file:
        #     batch_script_file.write(batch_script_content)
        #
        # batch_script_content = f'call "{venv_activate_script}" && python "{script2}"'
        # with open('temp_batch_script2.bat', 'w') as batch_script_file:
        #     batch_script_file.write(batch_script_content)
        #
        # # Run the temporary batch scripts
        # process1 = subprocess.Popen('temp_batch_script1.bat', shell=True)
        # process2 = subprocess.Popen('temp_batch_script2.bat', shell=True)
        #
        # process1.wait()
        # process2.wait()
        #
        # # Optionally, remove the temporary batch scripts
        # os.remove('temp_batch_script1.bat')
        # os.remove('temp_batch_script2.bat')

        process1 = subprocess.Popen(["program_icon.exe"])
        process2 = subprocess.Popen(["Count Time.exe"])
        process1.wait()
        process2.wait()
