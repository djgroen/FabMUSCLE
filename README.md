# FabMUSCLE
This is a dummy example plugin for FabSim3. It is meant to showcase a minimal implementation for a FabSim3 plugin.

## Installation
Simply type `fabsim localhost install_plugin:FabMUSCLE` anywhere inside your FabSim3 install directory.

## Testing
1. To run a unified MUSCLE test job, type `fabsim localhost muscle_unified:muscle_rd_test,muscle_script=reaction_diffusion.py`.
1. To run a unified MUSCLE test job replicated 5 times (all identical), type `fabsim localhost muscle_unified:muscle_rd_test,muscle_script=reaction_diffusion.py,replicas=5`.

## Explanation of files
* FabMUSCLE.py - main file containing the ```fabsim localhost dummy``` command implementation.
* config_files/muscle_rd_test - directory containing input data for the one file reaction diffusion test application.
* config_files/muscle_rd_distr_test - directory containing input data for the distributed reaction diffusion test application.
* templates/muscle_unified - template file for running all-in-one muscle scripts on the remote machine.
* templates/muscle_manager - template file for running the MUSCLE3 manager on the remote machine.
* templates/muscle_model - template file for running individual MUSCLE3 model scripts on the remote machine.

