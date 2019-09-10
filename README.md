# FabMUSCLE

This is a preliminary launcher for the MUSCLE3 toolkit. It serves to
automatically set up MUSCLE3 simulations, launch the manager and its submodels,
and keep all the associated data organized.

## Installation
Simply type `fabsim localhost install_plugin:FabMUSCLE` anywhere inside your FabSim3 install directory.

## Installing MUSCLE3
On a local machine, just use `pip3 install muscle3`
On a remote machine where you don't have admin rights, you can use `fabsim <machine> install_muscle:install_muscle`


## Testing
1. To run a unified MUSCLE test job, type `fabsim localhost muscle_unified:muscle_rd_test,muscle_script=reaction_diffusion.py`.
1. To run a unified MUSCLE test job replicated 5 times (all identical), type `fabsim localhost muscle_unified:muscle_rd_test,muscle_script=reaction_diffusion.py,replicas=5`.
1. To run a distributed MUSCLE test job locally, type `fabsim localhost run_muscle_dist_local:muscle_rd_distr_test,ymmsl_name=reaction_diffusion.ymmsl`.

### In progress
We are currently working to enable:
1. `fabsim localhost run_muscle_dist:muscle_rd_distr_test,ymmsl_name=reaction_diffusion.ymmsl` (in localized job submission mode).
1. `fabsim eagle_vecma run_muscle_dist:muscle_rd_distr_test,ymmsl_name=reaction_diffusion.ymmsl` (with slurm job submission).
1. `fabsim eagle_vecma run_muscle_dist:muscle_rd_distr_test,ymmsl_name=reaction_diffusion.ymmsl,PilotJob=true` (with QCG pilot job submission).



## Explanation of files
* FabMUSCLE.py - main file containing the ```fabsim localhost dummy``` command implementation.
* config_files/muscle_rd_test - directory containing input data for the one file reaction diffusion test application.
* config_files/muscle_rd_distr_test - directory containing input data for the distributed reaction diffusion test application.
* templates/muscle_unified - template file for running all-in-one muscle scripts on the remote machine.
* templates/muscle_manager - template file for running the MUSCLE3 manager on the remote machine.
* templates/muscle_model - template file for running individual MUSCLE3 model scripts on the remote machine.
* templates/muscle_distributed - flexible template file for running any MUSCLE3 part on the remote machine.

