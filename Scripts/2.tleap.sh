
# Load the force field parameters and the water model
source leaprc.gaff
source leaprc.protein.ff14SB

# Load force field parameters
loadamberparams system1.frcmod
loadoff system1.lib
loadamberparams system2.frcmod
loadoff system2.lib
loadamberparams solvent.frcmod
loadamberprep solvent.prep

# Load the mol2 file
sys = loadPdb solvated.pdb

# Create the system
#solvateBox mol TIP3PBOX 10.0
setBox sys vdw 10.0

# Save the topology and coordinate files
saveamberparm sys system.parm system.rst
savepdb sys system.pdb
quit

