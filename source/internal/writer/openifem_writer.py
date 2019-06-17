import datetime
import string

import smtk
import smtk.model

import subwriter
from subwriter import subsection
reload(subwriter)


class OpenIFEMWriter:
    '''Top level writer for OpenIFEM (.prm) files
    '''

    def __init__(self, operator_spec):
        # get the specs
        # Get the attributes
        self.sim_atts = smtk.attribute.Resource.CastTo(
            operator_spec.find('attributes').value())
        # Get fluid model
        model_entity = smtk.model.Entity.CastTo(
            operator_spec.find('fluid_model').objectValue(0))
        self.fluid_model_resource = smtk.model.Resource.CastTo(
            model_entity.resource())
        # Get solid model
        model_entity = smtk.model.Entity.CastTo(
            operator_spec.find('solid_model').objectValue(0))
        self.solid_model_resource = smtk.model.Resource.CastTo(
            model_entity.resource())
        print('sim_atts', self.sim_atts)
        if self.sim_atts is None:
            msg = 'ERROR - No simulation attributes'
            print(msg)
            raise Exception(msg)
        # Initialize the subsections
        self.subsections = list()
        self.subsections.append(
            subwriter.simulation_subsection('Simulation', self.sim_atts))
        self.subsections.append(subwriter.fluid_FE_subsection(
            'Fluid finite element system', self.sim_atts))
        self.subsections.append(subwriter.fluid_material_subsection(
            'Fluid material properties', self.sim_atts))
        self.subsections.append(subwriter.fluid_sc_subsection(
            'Fluid solver control', self.sim_atts))
        self.subsections.append(subwriter.fluid_dirichlet_subsection(
            'Fluid Dirichlet BCs', self.sim_atts, self.fluid_model_resource))
        self.subsections.append(subwriter.fluid_neumann_subsection(
            'Fluid Neumann BCs', self.sim_atts, self.fluid_model_resource))
        self.subsections.append(subwriter.solid_FE_subsection(
            'Solid finite element system', self.sim_atts))
        self.subsections.append(subwriter.solid_material_subsecion(
            'Solid material properties', self.sim_atts, self.solid_model_resource))
        self.subsections.append(subwriter.solid_sc_subsection(
            'Solid solver control', self.sim_atts))
        self.subsections.append(subwriter.solid_dirichlet_subsection(
            'Solid Dirichlet BCs', self.sim_atts, self.solid_model_resource))
        self.subsections.append(subwriter.solid_neumann_subsection(
            'Solid Neumann BCs', self.sim_atts, self.solid_model_resource))

    def cache_properties(self):
        for sec in self.subsections:
            sec.cache_properties()

    def write(self, out):
        for sec in self.subsections:
            sec.write(out)
