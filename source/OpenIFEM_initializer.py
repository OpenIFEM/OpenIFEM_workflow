'''
Initialization script for OpenIFEM workflows
'''


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
    import smtk.mesh
    import smtk.resource

reload(openifem_writer)
# ---------------------------------------------------


class Initialization(smtk.operation.Operation):
    def __init__(self):
        smtk.operation.Operation.__init__(self)

    def name(self):
        return "Initialize OpenIFEM"

    def operateInternal(self):
        try:
            result = InitializeOpenIFEM(self)
        except:
            print('Error', self.log().convertToString())
            raise

        return result

    def createSpecification(self):
        # Create a spec from smtk createBaseSpecification function
        spec = self.createBaseSpecification()
        print('spec', spec)

        # Load export atts
        source_dir = os.path.abspath(os.path.dirname(__file__))
        print('source_dir:', source_dir)
        sbt_path = os.path.join(source_dir, 'internal',
                                'OpenIFEM_initialize.sbt')
        print('sbt_path:', sbt_path)
        # Create a new attribute that stores the output specs
        reader = smtk.io.AttributeReader()
        result = reader.read(spec, sbt_path, self.log())
        print('reader result:', result)

        # Setup result definition
        # resultDef = spec.createDefinition('test result', 'result')
        # successDef = smtk.attribute.IntItemDefinition.New('success')
        # resultDef.addItemDefinition(successDef)

        return spec


def InitializeOpenIFEM(init_op):
    '''
    Entry function, called by CMB to import model file
    '''

    operator_spec = init_op.parameters()

    # Find mesh files
    solid_model_item = operator_spec.findFile('solid_model')
    fluid_model_item = operator_spec.findFile('fluid_model')
    dim_item = operator_spec.findInt('dimension')

    dim = dim_item.value(0)

    # Create new mesh session
    session = smtk.session.mesh.Session.create()
    if solid_model_item.isEnabled():
        # Get filepath
        solid_filepath = solid_model_item.value(0)

        # Create mesh resource
        resource = smtk.session.mesh.Resource.create()
        mesh_resource = smtk.mesh.Resource.create()
        resource.setSession(session)

        meshes = mesh_resource.meshes()
        # Get the mesh resource from file
        print('Load file from {}'.format(solid_model_item.value(0)))
        smtk.io.importMesh(
            solid_filepath, mesh_resource, 'Solid')
        if not mesh_resource or not mesh_resource.isValid():
            print('FAILED!\n')
        print('mesh_resource: %s' % mesh_resource)
        print('dir(mesh_resource): %s' % dir(mesh_resource))
        # try:
        #     mesh_resource.setName('Solid')
        # except:
        #     e = sys.exc_info()[0]
        #     print('setName? %s' % e)
        # resource.setName('Solid')
        mesh_resource.modelResource = resource
        resource.setMeshTessellations(mesh_resource)
        # Create a model
        model = resource.addModel(dim, dim)
        model.setName('Solid')
        session.addTopology(resource, smtk.session.mesh.Topology(
            model.entity(), meshes))
        model.setStringProperty('url', solid_filepath)
        model.setStringProperty('type', 'gmsh')

        session.declareDanglingEntity(model)

        mesh_resource.associateToModel(model.entity())

        model.setSession(smtk.model.SessionRef(
            resource, resource.session().sessionId()))

        # transcribe
        resource.session().transcribe(model, smtk.model.SESSION_EVERYTHING, False)
        #
        # Return the result
        result = init_op.createResult(
            smtk.operation.Operation.Outcome.SUCCEEDED)
        resultModels = result.findComponent('model')
        resultModels.setValue(model.component())
        created_resource = result.findResource('resource')
        created_resource.setValue(resource)
        created = result.findComponent('created')
        created.appendValue(model.component())
        result.findComponent('mesh_created').setValue(model.component())

        return result

    return 1
