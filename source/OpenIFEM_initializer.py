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
    import smtk.view

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

        # Import the models based on the analyses
        if solid_model_item.isEnabled():
            solid_analysis = True
            # Get filepath
            solid_filepath = solid_model_item.value(0)
            # Create session resource
            self.solid_resource = smtk.session.mesh.Resource.create()
            self.solid_resource.setSession(self.session)
            self.solid_resource.setName('Solid')
            # import solid model
            self.solid_model = self.import_model(
                solid_filepath, self.solid_resource, 'Solid')

        if fluid_model_item.isEnabled():
            fluid_analysis = True
            # Get filepath
            fluid_filepath = fluid_model_item.value(0)
            # Create session resource
            self.fluid_resource = smtk.session.mesh.Resource.create()
            self.fluid_resource.setSession(self.session)
            self.fluid_resource.setName('Fluid')
            # import solid model
            self.fluid_model = self.import_model(
                fluid_filepath, self.fluid_resource, 'Fluid')

        # Read the attribute
        source_dir = os.path.abspath(os.path.dirname(__file__))
        self.att_resource = smtk.attribute.Resource.create()
        reader = smtk.io.AttributeReader()
        sbt_path = os.path.join(source_dir, 'OpenIFEM.sbt')
        reader.read(self.att_resource, sbt_path, True, self.log())

        # Change the name
        self.att_resource.setName('Parameters')

        analyses = self.att_resource.analyses()
        analyses.buildAnalysesDefinition(
            self.att_resource, 'analysis', 'Analysis')
        analyses_def = self.att_resource.findDefinition('analysis')

        # Enable the analyses based on imported models
        if (solid_analysis):
            analyses_def.itemDefinition(1).setIsEnabledByDefault(True)
        if (fluid_analysis):
            analyses_def.itemDefinition(0).setIsEnabledByDefault(True)

        # Print out views and definitions in the attribute resource
        views = self.att_resource.views()
        for v in views:
            print('View: %s' % v)
        defs = self.att_resource.definitions()
        for d in defs:
            print('Def: %s' % d.type())

        # Change the gravity component and entity filters according to the dimension
        if self.dim == 3:
            # Change default dimension
            self.att_resource.findDefinition(
                'simulation').itemDefinition(0).setDefaultDiscreteIndex(1)
            # Change gravity input
            self.att_resource.findDefinition(
                'simulation').itemDefinition(7).setNumberOfRequiredValues(3)
            # Change entity filter
            self.att_resource.findDefinition(
                'fluid_boundary_conditions').clearLocalAssociationRule()
            self.att_resource.findDefinition(
                'fluid_boundary_conditions').createLocalAssociationRule()
            self.att_resource.findDefinition('fluid_boundary_conditions').localAssociationRule(
            ).setAcceptsEntries('smtk::model::Resource', "edge[ string { 'Analysis' = 'Fluid' }]", True)
            self.att_resource.findDefinition(
                'solid_boundary_conditions').clearLocalAssociationRule()
            self.att_resource.findDefinition(
                'solid_boundary_conditions').createLocalAssociationRule()
            self.att_resource.findDefinition('solid_boundary_conditions').localAssociationRule(
            ).setAcceptsEntries('smtk::model::Resource', "edge[ string { 'Analysis' = 'Solid' }]", True)
            self.att_resource.findDefinition(
                'solid_materials').clearLocalAssociationRule()
            self.att_resource.findDefinition(
                'solid_materials').createLocalAssociationRule()
            self.att_resource.findDefinition('solid_materials').localAssociationRule(
            ).setAcceptsEntries('smtk::model::Resource', "face[ string { 'Analysis' = 'Solid' }]", True)

        if self.dim == 2:
            # Remove the z component in BCs (actually hide it)
            self.att_resource.findDefinition('fluid_dirichlet').itemDefinition(
                0).itemDefinition(2).setAdvanceLevel(11)
            self.att_resource.findDefinition('solid_dirichlet').itemDefinition(
                0).itemDefinition(2).setAdvanceLevel(11)
            # Change entity filter
            self.att_resource.findDefinition(
                'fluid_boundary_conditions').clearLocalAssociationRule()
            self.att_resource.findDefinition(
                'fluid_boundary_conditions').createLocalAssociationRule()
            self.att_resource.findDefinition('fluid_boundary_conditions').localAssociationRule(
            ).setAcceptsEntries('smtk::model::Resource', "edge[ string { 'Analysis' = 'Fluid' }]", True)
            self.att_resource.findDefinition(
                'solid_boundary_conditions').clearLocalAssociationRule()
            self.att_resource.findDefinition(
                'solid_boundary_conditions').createLocalAssociationRule()
            self.att_resource.findDefinition('solid_boundary_conditions').localAssociationRule(
            ).setAcceptsEntries('smtk::model::Resource', "edge[ string { 'Analysis' = 'Solid' }]", True)
            self.att_resource.findDefinition(
                'solid_materials').clearLocalAssociationRule()
            self.att_resource.findDefinition(
                'solid_materials').createLocalAssociationRule()
            self.att_resource.findDefinition('solid_materials').localAssociationRule(
            ).setAcceptsEntries('smtk::model::Resource', "face[ string { 'Analysis' = 'Solid' }]", True)

        # Generate the result
        result = self.createResult(
            smtk.operation.Operation.Outcome.SUCCEEDED)

        created_resource = result.findResource('resource')
        created_resource.appendValue(self.att_resource)

        resultModels = result.findComponent('model')
        created = result.findComponent('created')
        if solid_analysis:
            created_resource.appendValue(self.solid_resource)

            resultModels.appendValue(self.solid_model.component())

            created.appendValue(self.solid_model.component())
            created.setIsEnabled(True)

            result.findComponent('mesh_created').appendValue(
                self.solid_model.component())

        if fluid_analysis:
            created_resource.appendValue(self.fluid_resource)

            resultModels.appendValue(self.fluid_model.component())

            created.appendValue(self.fluid_model.component())
            created.setIsEnabled(True)

            result.findComponent('mesh_created').appendValue(
                self.fluid_model.component())

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

    def import_model(self, filepath, resource, model_name):
        # Create mesh resource
        mesh_resource = smtk.mesh.Resource.create()

        # Get the mesh resource from file
        print('Load file from {}'.format(filepath))
        smtk.io.importMesh(
            filepath, mesh_resource, model_name)

        # Get meshset for new mesh
        meshes = mesh_resource.meshes()

        # Remove the mesh without domains
        meshes_without_domains = []
        for i in range(meshes.size()):
            submesh = meshes.subset(i)
            if len(submesh.domains()) == 0:
                meshes_without_domains.append(submesh)

        for mesh_without_domain in meshes_without_domains:
            mesh_resource.removeMeshes(mesh_without_domain)

        # If no mesh found return failue message
        if not mesh_resource or not mesh_resource.isValid():
            return self.createResult(smtk.operation.Operation.Outcome.FAILED)

        # Set name on mesh and resource
        mesh_resource.setName(model_name)

        # Set association between resource and mesh resource
        mesh_resource.modelResource = resource
        resource.setMeshTessellations(mesh_resource)

        # Create a model
        model = resource.addModel(self.dim, self.dim)
        model.setName(model_name)

        # Construct the topology
        self.session.addTopology(resource, smtk.session.mesh.Topology(
            model.entity(), meshes, False))

        model.setStringProperty('url', filepath)
        model.setStringProperty('type', 'gmsh')

        self.session.declareDanglingEntity(model)

        model.setSession(smtk.model.SessionRef(
            resource, self.session.sessionId()))

        mesh_resource.associateToModel(model.entity())

        # transcribe
        resource.session().transcribe(
            model, smtk.model.SESSION_EVERYTHING, False)

        # Set string property to the model and its entities
        model.setStringProperty('Analysis', model_name)
        entities = model.cells()
        for e in entities:
            e.setStringProperty('Analysis', model_name)

        # Rename model entities
        # The bitflag 100 indicates all the edges, faces and volumes
        sub_entities = resource.findEntitiesOfType(0x00000100)
        for entity in sub_entities:
            # Edge entities
            if entity.entityFlags() == 0x00000102:
                new_name = re.sub('Domain', model_name +
                                  ' Edge', entity.name())
                entity.setName(new_name)
            # Face entities
            elif entity.entityFlags() == 0x00000104:
                new_name = re.sub('Domain', model_name +
                                  ' Face', entity.name())
                entity.setName(new_name)
            # Volume entities
            elif entity.entityFlags() == 0x00000108:
                new_name = re.sub('Domain', model_name +
                                  ' Volume', entity.name())
                entity.setName(new_name)

        return model
