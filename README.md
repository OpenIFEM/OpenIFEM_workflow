# OpenIFEM_workflow

This is a CMB (https://gitlab.kitware.com/cmb) workflow for OpenIFEM (https://github.com/OpenIFEM/OpenIFEM).

*Note: Since OpenIFEM is a library, there is not a universal binrary file that handles all the simulation settings, at least for now. You may still need to write the c++ program to execute a specific simulation.*

## Installation

You can download CMB binray at (https://www.computationalmodelbuilder.org/download/)

If you would like to build CMB from source, take a look at CMB superbuild: (https://gitlab.kitware.com/cmb/cmb-superbuild)


## How to use `OpenIFEM.sbt` file

1. In CMB modelbuilder, import the parameters template by clicking Open and select `OpenIFEM.sbt.`

2. Load model and edit the simulation specs in attribute editor.

3. Click on `export simulation` and select OpenIFEM.py file to export parameters file.

4. Run your simulation.

5. You can visualize the results by enablig `vtkpostprocesingmodule` in module manager.

## How to initialize an OpenIFEM project with `OpenIFEM.initializer`

1. In modeulbuilder, click on `import operation` and import OpenIFEM_initializer.py

2. An operator named `OpenIFEM.initializer` will appear in operations list.

3. Open the operator, select the dimension, solid and fluid models to be imported.

4. The initializer will choose the analysis based on whether you imported a solid model (solid analysis), fluid model (fluid analysis), or both (FSI analysis). The dimension setting in the attribute resource will be frozen once you create the workflow.

5. You can assign solid and fluid BC, and solid material on the corresponding models, set the parameters and export the parameters file.
