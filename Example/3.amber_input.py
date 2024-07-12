import os
import subprocess

print()
print()

# Get user input for min, heat, and equil

# Define the input file template for minimization
min_template = "minimize\n"\
"&cntrl\n"\
"  imin = 1,\n"\
"  irest=0,\n"\
"  maxcyc = {maxcyc},\n"\
"  ncyc = {ncyc},\n"\
"  ntpr = 50,\n"\
"  ntx = 1,\n"\
"  ntwx = 0,\n"\
"  cut = {cut},\n"\
"  igb =0,\n"\
"  ntwr = {ntwr},\n"\
"/\n"\
" "

# Define the input file template for heating
heat1_template = "&cntrl\n"\
"  imin = 0,\n"\
"  ntx = 1,\n"\
"  irest = 0,\n"\
"  ntc = 2,\n"\
"  ntf = 2,\n"\
"  tol = 0.0000001,\n"\
"  cut = {cut},\n"\
"  nstlim = 25000,\n"\
"  dt = {dt},\n"\
"  ntwx = {ntwx},\n"\
"  ntwr = {ntwr},\n"\
"  ntt = 3,\n"\
"  gamma_ln = 1000.0,\n"\
"  ntr = 1,\n"\
"  ig = -1,\n"\
"  ntpr = 100,\n"\
"  nmropt = 1,\n"\
"  ntb = 2,\n"\
"  taup = 2.0,\n"\
"  ioutfm = 1,\n"\
"  ntxo = 2,\n"\
"  ntp = 2,\n"\
"/\n"\
"\n"\
"&wt type='TEMP0',\n"\
"    istep1 = 0,\n"\
"    istep2 = 25000,\n"\
"    value1 = 0.0,\n"\
"    value2 = 100.0\n"\
"/\n"\
"\n"\
"&wt type='END'\n"\
"/\n"\
"Hold system fixed\n"\
"10.0\n"\
"RES 1 2\n"\
"END\n"\
"END\n"
" "

heat2_template = "&cntrl\n"\
"  imin = 0,\n"\
"  ntx = 5,\n"\
"  irest = 1,\n"\
"  ntc = 2,\n"\
"  ntf = 2,\n"\
"  tol = 0.0000001,\n"\
"  cut = {cut},\n"\
"  nstlim = {nstlim},\n"\
"  dt = {dt},\n"\
"  ntwx = {ntwx},\n"\
"  ntwr = {ntwr},\n"\
"  ntt = 3,\n"\
"  gamma_ln = 1.0,\n"\
"  ntr = 1,\n"\
"  ig = -1,\n"\
"  ntpr = 100,\n"\
"  nmropt = 1,\n"\
"  ntb = 2,\n"\
"  taup = 2.0,\n"\
"  ioutfm = 1,\n"\
"  ntxo = 2,\n"\
"  ntp = 2,\n"\
"/\n"\
"\n"\
"&wt type='TEMP0',\n"\
"    istep1 = 0,\n"\
"    istep2 = 50000,\n"\
"    value1 = 100.0,\n"\
"    value2 = {temp1}\n"\
"/\n"\
"\n"\
"&wt type='END'\n"\
"/\n"\
"Hold system fixed\n"\
"10.0\n"\
"RES 1 2\n"\
"END\n"\
"END\n"
" "


# Define the input file template for equilibration
equil_template = "Equilibration\n"\
" &cntrl\n"\
"  imin=0,\n"\
"  ntx=5,\n"\
"  irest=1,\n"\
"  ntc=2,\n"\
"  ntf=2,\n"\
"  tol=0.0000001,\n"\
"  ntt=3,\n"\
"  gamma_ln=1.0,\n"\
"  temp0={temp0},\n"\
"  ig = -1,\n"\
"  ntpr=1000,\n"\
"  ntwr={ntwr},\n"\
"  ntwx={ntwx},\n"\
"  nstlim={nstlim},\n"\
"  dt={dt},\n"\
"  ntb=2,\n"\
"  cut={cut},\n"\
"  ioutfm=1,\n"\
"  ntxo=2,\n"\
"  nmropt=1,\n"\
"  ntp=3,\n"\
"  csurften=3,\n"\
"  gamma_ten=0.0,\n"\
"  ninterface=2,\n"\
"/\n"\
" &wt type='DUMPFREQ', istep1=1000 /\n"\
" &wt type='END', /\n"\
"DISANG=COM_dist.RST\n"\
"DUMPAVE=dist.dat\n"\
"LISTIN=POUT\n"\
"LISTOUT=POUT\n"\
"/\n"\
"/\n"\
" &ewald\n"\
"  skinnb=3.0,\n"\
" /\n"\
"  "
# Define the input file template for pulling
pull_template = " &cntrl\n"\
"   imin=0,\n"\
"   ntx=5,\n"\
"   irest=1,\n"\
"   ntc=2,\n"\
"   ntf=2,\n"\
"   tol=0.0000001,\n"\
"   nstlim={nstlim},\n"\
"   ntt=3,\n"\
"   gamma_ln=1.0,\n"\
"   temp0={temp0},\n"\
"   ntpr=1000,\n"\
"   ntwr={ntwr},\n"\
"   ntwx={ntwx},\n"\
"   dt={dt},\n"\
"   ig=-1,\n"\
"   ntb=2,\n"\
"   cut={cut},\n"\
"   ioutfm=1,\n"\
"   ntxo=2,\n"\
"   nmropt=1,\n"\
"   ntp=3,\n"\
"   csurften=3,\n"\
"   gamma_ten=0.0,\n"\
"   ninterface=2,\n"\
"   jar=1,\n"\
" /\n"\
" &wt type='DUMPFREQ', istep1=1000 /\n"\
" &wt type='END', /\n"\
"DISANG=COM_pull.RST\n"\
"DUMPAVE=Pull_dist.dat\n"\
"LISTIN=POUT\n"\
"LISTOUT=POUT\n"\
"/\n"\
"/\n"\
" &ewald\n"\
"   skinnb=3.0,\n"\
" /\n"

# Define the input file template for umbrella sampling
prod_template = "Umbrella-sampling\n"\
" &cntrl\n"\
"  imin=0,\n"\
"  ntx=1,\n"\
"  irest=0,\n"\
"  ntc=2,\n"\
"  ntf=2,\n"\
"  tol=0.0000001,\n"\
"  ntt=3,\n"\
"  gamma_ln=1.0,\n"\
"  temp0={temp0},\n"\
"  ig = -1,\n"\
"  ntpr=1000,\n"\
"  ntwr={ntwr},\n"\
"  ntwx={ntwx},\n"\
"  nstlim={nstlim},\n"\
"  dt={dt},\n"\
"  ntb=2,\n"\
"  cut={cut},\n"\
"  ioutfm=1,\n"\
"  ntxo=2,\n"\
"  nmropt=1,\n"\
"  ntp=3,\n"\
"  csurften=3,\n"\
"  gamma_ten=0.0,\n"\
"  ninterface=2,\n"\
"/\n"\
" &wt type='DUMPFREQ', istep1=500 /\n"\
" &wt type='END', /\n"\
"DISANG=COM_prod.RST\n"\
"DUMPAVE=dist.dat\n"\
"LISTIN=POUT\n"\
"LISTOUT=POUT\n"\
"/\n"\
"/\n"\
" &ewald\n"\
"  skinnb=3.0,\n"\
" /\n"\
"  "


# Define the input file generator function
def generate_input_file(template, **kwargs):
    # Replace the placeholders with the provided values
    for key, value in kwargs.items():
        template = template.replace("{"+key+"}", str(value))
    return template

# Generate the input files for minimization, heating, and equilibration
min_input = generate_input_file(min_template, maxcyc=1000, ncyc=5000, cut=10.0, ntwr=2000)
heat1_input = generate_input_file(heat1_template, temp1=300.0, cut=10.0, dt=0.00005, ntwx=100, ntwr=1000,)
heat2_input = generate_input_file(heat2_template, temp1=300.0, cut=10.0, nstlim=10000, dt=0.002, ntwx=100, ntwr=1000,)
equil_input = generate_input_file(equil_template, temp0=300.0, cut=10.0, nstlim=50000, dt=0.002, ntwx=500, ntwr=500,)
pull_input = generate_input_file(pull_template, temp0=300.0, cut=10.0, nstlim=32000, dt=0.002, ntwx=500, ntwr=1000,)
prod_input = generate_input_file(prod_template, temp0=300.0, cut=10.0, nstlim=1000000, dt=0.002, ntwx=1000, ntwr=1000,)

# Write the input files to disk
with open('min.in', 'w') as f:
    f.write(min_input)
with open('heat1.in', 'w') as f:
    f.write(heat1_input)
with open('heat2.in', 'w') as f:
    f.write(heat2_input)
with open('equil.in', 'w') as f:
    f.write(equil_input)
with open('pull.in', 'w') as f:
    f.write(pull_input)
with open('prod.in', 'w') as f:
    f.write(prod_input)


chosen_parm = "system.parm"
chosen_rst = "system.rst"


# Generate the submission file
script = """#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --partition=day-long
#SBATCH --nodes=1
#SBATCH --mem=5G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
echo $HOSTNAME

export LD_LIBRARY_PATH=/home/shared_write/gcc/installation/lib64:$LD_LIBRARY_PATH
export PATH=/home/shared_write/gcc/installation/bin:$PATH
bash /home/shared_write/gcc/amber_cuda/amber-interactive.sh

#--------------------------------------------------------------#

pmemd.cuda -O -i min.in -c {chosen_rst} -p {chosen_parm} -r min.rst -x min.nc -o min.out -inf min.info
pmemd.cuda -O -i heat1.in -o heat1.out -p {chosen_parm} -c min.rst -r heat1.rst -x heat1.nc -ref min.rst
pmemd.cuda -O -i heat2.in -o heat2.out -p {chosen_parm} -c heat1.rst -r heat2.rst -x heat2.nc -ref heat1.rst
pmemd.cuda -O -i equil.in -o equil.out -p {chosen_parm} -c heat2.rst -r equil.rst -x equil.nc -inf equil.info
pmemd.cuda -O -i pull.in -o pull.out -p {chosen_parm} -c equil.rst -r pull.rst -x pull.nc -inf pull.info
"""

# Substitute the chosen_file variable in the submission script
script = script.format(chosen_rst=chosen_rst, chosen_parm=chosen_parm)

# Write the script to a file
with open("amber.sh", "w") as f:
    f.write(script)


# Generate the disang file from user input



def count_atoms(filename):
    with open(filename, "r") as file:
        num_atoms = 0
        for line in file:
            if line.startswith("ATOM"):
                num_atoms += 1
    return num_atoms

def main():
    global igr1, igr2  # Declare igr1 and igr2 as global variables
    filename_bdp = "system1.pdb"
    filename_btb = "system2.pdb"

    # Step 1: Count the number of atoms in the bdp.pdb file
    num_atoms_bdp = count_atoms(filename_bdp)

    # Step 2: Create the igr1 variable as a string with values separated by commas and a trailing comma
    igr1 = ",".join(str(val) for val in range(1, num_atoms_bdp + 1))

    # Step 3: Count the number of atoms in the btb.pdb file
    num_atoms_btb = count_atoms(filename_btb)

    # Step 4: Create the igr2 variable as a string with values after igr1 and a trailing comma
    igr2_start = num_atoms_bdp + 1
    igr2_end = igr2_start + num_atoms_btb
    igr2 = ",".join(str(val) for val in range(igr2_start, igr2_end))

if __name__ == "__main__":
    main()



# You can now use igr1 and igr2 as needed for the rest of your script.
# For example, you can use them to generate the restraint strings like you did before.





#igr1 = input("Enter the atom number for COM1 with comma-separated, igr1: ")
#igr2 = input("Enter the atom number for COM2 with comma-separated, igr2: ")
#r2 = float(input("Enter the minimum distance value for the pulling (in A): "))
#r2a = float(input("Enter the maximum distance value for the pulling (in A): "))
#rk2 = float(input("Enter the force constant value, rk2: "))
r2 = 0.3
r2a = 32.3
rk2 = 1.0
rk3 = 2.0
r1 = r2-30
r4 = r2a+30

# Create the script with user input variables
disang_equi = f"""
&rst
iat=-1,-1,
r1={r1},
r2={r2},
r3={r2},
r4={r4},
rk2={rk2},
rk3={rk2},
igr1={igr1},
igr2={igr2},
/
"""

disang_pull = f"""
&rst
iat=-1,-1,
r2={r2},
rk2={rk2},
r2a={r2a},
igr1={igr1},
igr2={igr2},
/
"""

disang_prod = f"""
&rst
iat=-1,-1,
r1={r1},
r2=dishere,
r3=dishere,
r4={r4},
rk2={rk3},
rk3={rk3},
igr1={igr1},
igr2={igr2},
/
"""

# Write the script to a file
with open("COM_dist.RST", "w") as f:
    f.write(disang_equi)

# Write the script to a file
with open("COM_pull.RST", "w") as f:
    f.write(disang_pull)

# Write the script to a file
with open("COM_prod.RST", "w") as f:
    f.write(disang_prod)

# Write frame.cpptraj file for extracting restart file for each window
frame = 32000/500 #since ntwx=500 for pulling
frame_diff = frame/32   #32 is the number of window

with open('frame.cpptraj', 'w') as f:
    f.write("""parm system.parm
trajin pull.nc\n""")
    for i in range(1, 33):
        f.write(f"trajout fram{i}.rst restart onlyframes {int((2*i-1)*frame_diff/2)}\n")
    f.write("""go
quit\n""")


# Define the path to your amber.sh script
script_path = "./amber.sh"

# Use subprocess to submit the job
subprocess.run(["sbatch", script_path])



