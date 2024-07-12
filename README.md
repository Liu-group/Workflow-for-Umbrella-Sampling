# Workflow-for-Umbrella-Sampling

## Overview

This project provides an automated protocol for Umbrella Sampling Simulation which generates potential mean forces (PMF) as function of COM distance of the interested molecules. By following this protocol, users can efficiently generate PMF profile from their XYZ coordinates or pdb file. 

![Alt text](./image.png)

The process involves several steps, including setting up AutoSolvate virtual environment, installing necessary dependencies, running the main script to generate a solvent box, minimization, heating, equilibration, pulling, constrained MD simulation and finally histrogram analysis with WHAM. These steps are designed to streamline the workflow and provide a comprehensive solution for generation PMF profile.

## Authors

Mohammad Pabel Kabir, Fang Liu

## Requirements

> AMBER16 or above

> AutoSolvate (https://autosolvate.readthedocs.io/en/latest/)

> Packmol (https://m3g.github.io/packmol/)

> WHAM (http://membrane.urmc.rochester.edu/content/wham)

## Workflow Description

### Step 1: Parameter File Generation for Individual Systems

Prepare a starting coordinates file (pdb or xyz) for the molecules for which you would like to generate an AIIM. Use antechamber to create AMBER parameters for the two systems and the solvent. Here, we use the example of BODIPY (system1) and TPAB (system2) molecules in ACN solvent:

antechamber -i system1.pdb -fi pdb -o system1.mol2 -fo mol2 -c bcc -s 2

antechamber -i system2.pdb -fi pdb -o system2.mol2 -fo mol2 -c bcc -s 2

antechamber -i solvent.pdb -fi pdb -o solvent.mol2 -fo mol2 -c bcc -s 2

Convert the resulting mol2 into an AMBER library file: tleap -f convert.leap

After this, you should have the following files: solvent.frcmod, solvent.prep, solvent.pdb, system1.lib, system1.frcmod, system1.pdb, system2.lib, system2.frcmod, system2.pdb

Note: Since both BODIPY and TPAB molecules contain a boron (B) atom, and the parameter for the B atom is not available in the Gaff force field, force field fitting is required. For our case, we did force field fitting to generate the parameter files.

### Step 2: Solvent Box and Parameter Generation for the Whole System

Generate solvent box coordinates using the packmol.py script, which employs Packmol to place system1 and system2 in the solvent and creates a solvated.pdb file:

python 1.packmol.py

Generate parameter file for the whole system with the tleap.sh script, which uses tleap tools, loads parameter files for individual systems and generate parameter file for the whole system:

tleap -f 2.tleap.sh

This will generate system.pdb, system.parm, and system.rst files

Note: Step 1 and Step 2 can be done with our in-house automated software AutoSolvate.

### Step 3: Minimization, Heating and Equilibration

Perform system minimization, heating, and equilibration for 100ps.

python 3.amber_input.py

### Step 4: Initial Configuration Generation and Geometry Optimization

Take snapshots every 1ps from the equilibration trajectory file. The snapshots will be used as guess structrues for ab-initio geometry optimization. 

python 4.guess_structrue_optimization.py

### Step 5: Desity Calculation and Normalization

Calculate center of mass (COM) points of system2 molecule from the optimized geometry, calculate density of the COM points and Normalize.

python 5.make_pdb_from_opt.py

bash 6.align_BDP.sh

python 7.pdb_to_xyz.py

bash 8.vdw_surface.sh

### Step 6: Generation of .mol2 File and AIIM

Generate mol2 file, which can be opened with a visualization software like VMD.

python 9.generate_mol2.py

## Getting Started

To begin using this workflow, clone the repository and navigate to the root directory. Ensure that all required Python libraries (`NumPy`, `Cython`, `pyvdwsurface`, etc.) are installed. Follow the steps outlined in the README files within each directory to execute the workflow successfully.


## Contributions

Contributions to this workflow are welcome. If you have suggestions for improvement or encounter any issues, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for more details.
