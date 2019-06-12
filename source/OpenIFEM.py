"""
Export script for OpenIFEM workflows
"""

import smtk
import os
import sys

# Add the directory containing this file to the python module search list
import inspect  # NOQA: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))))

import internal  # NOQA: E402
from internal.writer import openifem_writer  # NOQA: E402

sys.dont_write_bytecode = True

if 'pybind11' == smtk.wrappingProtocol():
    import smtk.attribute
    import smtk.io
    import smtk.model
    import smtk.operation
    import smtk.session.mesh
    import smtk.simulation

reload(openifem_writer)
# ---------------------------------------------------


class Export(smtk.operation.Operation):
    # Export is really a derived class from smtk operation

    def __init__(self):
        smtk.operation.Operation.__init__(self)

    def name(self):
        return "Export OpenIFEM"

    def operateInternal(self):
        try:
            success = ExportCMB(self)
        except:
            print('Error', self.log().convertToString())
            raise

        # Return with success
        result = self.createResult(smtk.operation.Operation.Outcome.SUCCEEDED)
        result.find('success').setValue(success)
        return result

    def createSpecification(self):
        # Create a spec from smtk createBaseSpecification function
        spec = self.createBaseSpecification()
        print('spec', spec)

        # Load export atts
        source_dir = os.path.abspath(os.path.dirname(__file__))
        print('source_dir:', source_dir)
        sbt_path = os.path.join(source_dir, 'internal', 'OpenIFEM_export.sbt')
        print('sbt_path:', sbt_path)
        # Create a new attribute that stores the output specs
        reader = smtk.io.AttributeReader()
        result = reader.read(spec, sbt_path, self.log())
        print('reader result:', result)

        # Setup result definition
        resultDef = spec.createDefinition('test result', 'result')
        successDef = smtk.attribute.IntItemDefinition.New('success')
        resultDef.addItemDefinition(successDef)

        return spec


def ExportCMB(export_op):
    '''
    Entry function, called by CMB to write export file
    '''

    operator_spec = export_op.parameters()
    logger = export_op.log()

    # Get output filename
    output_file_item = operator_spec.findFile('parameters_file')
    output_file = output_file_item.value(0)
    output_dir = os.path.dirname(output_file)

    # Create output folder if needed
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize OpenIFEM writer
    file_writer = openifem_writer.OpenIFEMWriter(operator_spec)
    file_writer.cache_properties()

    # Open the file
    with open(output_file, 'w') as out:
        out.write('# Generated from CMB\n')
        out.write('# This is an OpenIFEM parameters file.\n')
        file_writer.write(out)

    print("Output dir:", output_dir)
    return 1
