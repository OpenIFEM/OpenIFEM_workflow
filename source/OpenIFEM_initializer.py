'''
Initialization script for OpenIFEM workflows
'''


import smtk
import os
import sys
import re

# Add the directory containing this file to the python module search list
import inspect  # NOQA: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))))

sys.dont_write_bytecode = True

if 'pybind11' == smtk.wrappingProtocol():
    import smtk.attribute
    import smtk.io
    import smtk.model
    import smtk.operation
    import smtk.session.mesh
    import smtk.mesh
    import smtk.resource

# ---------------------------------------------------


class Initialization(smtk.operation.Operation):
    def __init__(self):
        smtk.operation.Operation.__init__(self)

    def name(self):
        return "Initialize OpenIFEM"

    def operateInternal(self):
        operator_spec = self.parameters()

        # Find mesh files
        solid_model_item = operator_spec.findFile('solid_model')
        fluid_model_item = operator_spec.findFile('fluid_model')
        dim_item = operator_spec.findInt('dimension')
        self.dim = dim_item.value(0)

        # Flags for analyses
        solid_analysis = False
        fluid_analysis = False

        # Create new mesh session
        self.session = smtk.session.mesh.Session.create()
        self.resource = smtk.session.mesh.Resource.create()
        self.resource.setSession(self.session)
        self.resource.setName('Models')

        # Create mesh resource
        self.mesh_resource = smtk.mesh.Resource.create()

        # Import the models based on the analyses
        if solid_model_item.isEnabled():
            solid_analysis = True
            # Get filepath
            solid_filepath = solid_model_item.value(0)
            # import solid model
            self.solid_model = self.import_model(solid_filepath, 'Solid')

        if fluid_model_item.isEnabled():
            fluid_analysis = True
            # Get filepath
            fluid_filepath = fluid_model_item.value(0)
            # import solid model
            self.fluid_model = self.import_model(fluid_filepath, 'Fluid')

        # Rename and remove model entities
        # The bigflag 100 indicates all the edges, faces and volumes
        sub_entities = self.resource.findEntitiesOfType(0x00000100)
        for entity in sub_entities:
            # Remove the abundant entities, only leave the physical domains.
            if re.match('edge', entity.name()) or re.match('face', entity.name()) or re.match('volume', entity.name()):
                self.resource.erase(entity)
                continue
            # Edge entities
            elif entity.entityFlags() == 0x00000102:
                new_name = re.sub('Domain', 'Edge', entity.name())
                entity.setName(new_name)
            # Face entities
            elif entity.entityFlags() == 0x00000104:
                new_name = re.sub('Domain', 'Face', entity.name())
                entity.setName(new_name)
            # Volume entities
            elif entity.entityFlags() == 0x00000108:
                new_name = re.sub('Domain', 'Volume', entity.name())
                entity.setName(new_name)

        # Generate the result
        result = self.createResult(
            smtk.operation.Operation.Outcome.SUCCEEDED)

        created_resource = result.findResource('resource')
        created_resource.setValue(self.resource)

        resultModels = result.findComponent('model')
        created = result.findComponent('created')
        if fluid_analysis:
            resultModels.appendValue(self.fluid_model.component())

            created.appendValue(self.fluid_model.component())
            created.setIsEnabled(True)

            result.findComponent('mesh_created').appendValue(
                self.fluid_model.component())
        if solid_analysis:
            resultModels.appendValue(self.solid_model.component())

            created.appendValue(self.solid_model.component())
            created.setIsEnabled(True)

            result.findComponent('mesh_created').appendValue(
                self.solid_model.component())

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

        return spec

    def import_model(self, filepath, model_name):
        # Get mesh set for old mesh
        preexisting_meshes = self.mesh_resource.meshes()

        # Get the mesh resource from file
        print('Load file from {}'.format(filepath))
        smtk.io.importMesh(
            filepath, self.mesh_resource, model_name)

        # Get meshset for new mesh
        allmeshes = self.mesh_resource.meshes()
        newmeshes = smtk.mesh.set_difference(allmeshes, preexisting_meshes)

        # If no mesh found return failue message
        if not self.mesh_resource or not self.mesh_resource.isValid():
            return self.createResult(smtk.operation.Operation.Outcome.FAILED)

        # Set name on mesh and resource
        self.mesh_resource.setName(model_name)

        # Set association between resource and mesh resource
        self.mesh_resource.modelResource = self.resource
        self.resource.setMeshTessellations(self.mesh_resource)

        # Create a model
        model = self.resource.addModel(self.dim, self.dim)
        model.setName(model_name)

        # Construct the topology
        self.session.addTopology(self.resource, smtk.session.mesh.Topology(
            model.entity(), newmeshes, False))

        model.setStringProperty('url', filepath)
        model.setStringProperty('type', 'gmsh')

        self.session.declareDanglingEntity(model)

        model.setSession(smtk.model.SessionRef(
            self.resource, self.session.sessionId()))

        self.mesh_resource.associateToModel(model.entity())

        # transcribe
        self.resource.session().transcribe(
            model, smtk.model.SESSION_EVERYTHING, False)

        # Set string property to the model and its entities
        model.setStringProperty('Analysis', model_name)
        entities = model.cells()
        for e in entities:
            e.setStringProperty('Analysis', model_name)

        return model
