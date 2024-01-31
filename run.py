import subprocess
import os

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
