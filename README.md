# OpenIFEM_workflow

This is a CMB (https://gitlab.kitware.com/cmb) workflow for OpenIFEM (https://github.com/OpenIFEM/OpenIFEM).

## Installation

1. Download Qt5 (https://www.qt.io/)
2. Using chmod to convert the downloaded file to executable, then run it to install:
```bash
chmod +x qt-unified-linux-x64-3.1.1-online.run
./qt-unified-linux-x64-3.1.1-online.run
```
2. Install CMB-superbuild (https://gitlab.kitware.com/cmb/cmb-superbuild) following instructions
```bash
git clone https://gitlab.kitware.com/cmb/cmb-superbuild.git
```
## How to use it
1. In CMB modelbuilder, import the parameters template by clicking Open and select OpenIFEM.sbt.

2. Load model and edit the simulation specs in attribute editor.

3. Click on "export simulation" and select OpenIFEM.py file to export parameters file.

4. Run your simulation.

5. You can visualize the results by enablig vtkpostprocesingmodule in module manager.
