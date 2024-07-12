# Run packmol
import subprocess

with open('packmol.inp', 'w') as f:
    f.write("# All atoms from diferent molecules will be at least 0.8 Angstroms apart\n")
    f.write("tolerance 0.8\n")
    f.write("\n")
    f.write("filetype pdb\n")
    f.write("\n")
    f.write("output solvated.pdb\n")
    f.write("\n")
    f.write("# add the solute\n")
    f.write("structure system1.pdb\n")
    f.write("   number 1\n")
    f.write("   fixed  40.0 40.0 40.0 0. 0. 0.\n")
    f.write("   centerofmass\n")
    f.write("   resnumbers 2\n")
    f.write("end structure\n")
    f.write("\n")
    f.write("# add the solute\n")
    f.write("structure system2.pdb\n")
    f.write("   number 1\n")
    f.write("   fixed  50.0 50.0 50.0 0. 0. 0.\n")
    f.write("   centerofmass\n")
    f.write("   resnumbers 2\n")
    f.write("end structure\n")
    f.write("# add first type of solvent molecules\n")
    f.write("structure solvent.pdb\n")
    f.write("  number 5900\n")
    f.write("  inside cube 0. 0. 0. 80.0\n")
    f.write("  resnumbers 2\n")
    f.write("end structure\n")

subprocess.run('packmol < packmol.inp', shell=True)

def add_ter(pdbfile:str):
    data   = open(pdbfile,'r').readlines()
    output = open(pdbfile,'w')
    this_resid = 1
    last_resid = 1
    for line in data:
        if 'ATOM' in line:
            last_resid = int(this_resid)
            this_resid = int(line[22:26])
        if last_resid != this_resid:
            output.write("TER\n")
        output.write(line)
    output.close()

add_ter('solvated.pdb')

# Run the amber-interactive.sh script using subprocess
subprocess.run(["bash", "/home/shared_write/gcc/amber_cuda/amber-interactive.sh"], check=True)
