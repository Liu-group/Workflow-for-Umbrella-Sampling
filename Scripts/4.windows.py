import os
import subprocess
# From pulling trajectory, 33 configuration were seleting at 0.1nm intervals
command = ['cpptraj', 'frame.cpptraj']
result = subprocess.run(command, capture_output=True, text=True)
# Initialize an empty list to store the job IDs
job_ids = []
os.system('cp equil.rst fram0.rst')
for i in range(0, 33, 1):
    # Create directory
    os.makedirs(f"dist_{i}")
    # Move required files
    os.chdir(f"./dist_{i}")
    os.system("cp ../COM_prod.RST .")
    os.system("cp ../amber.sh .")
    os.system("cp ../prod.in .")
    os.system(f"cp ../fram{i}.rst .")
    os.system("cp ../system.parm .")
    # Replace DISTHERE with i in COM_dist.RST
    with open("COM_prod.RST", "r") as f:
        contents = f.read()
    contents = contents.replace("dishere", str(i))
    with open("COM_prod.RST", "w") as f:
        f.write(contents)
    # Add command to amber.sh
    with open("amber.sh", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        f.writelines(lines[:-12])
        f.write(f"pmemd.cuda -O -i prod.in -o prod_{i}.out -p *.parm -c fram{i}.rst -r prod_{i}.rst -x prod_{i}.nc -inf prod_{i}.mdinfo\n")
    # Define the path to your amber.sh script
    script_path = "./amber.sh"
    # Use subprocess to submit the job and capture the job ID
    result = subprocess.run(["sbatch", script_path], capture_output=True, text=True)
    job_id = result.stdout.strip().split()[-1]
    job_ids.append(job_id)
    #Go back to parent directory
    os.chdir("../")
