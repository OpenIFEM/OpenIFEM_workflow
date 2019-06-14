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
        self.sim_atts = smtk.attribute.Resource.CastTo(
            operator_spec.find('attributes').value())
        model_entity = smtk.model.Entity.CastTo(
            operator_spec.find('model').objectValue(0))
        self.model_resource = smtk.model.Resource.CastTo(
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
            'Fluid Dirichlet BCs', self.sim_atts, self.model_resource))
        self.subsections.append(subwriter.fluid_neumann_subsection(
            'Fluid Neumann BCs', self.sim_atts, self.model_resource))
        # self.subsections.append(subsection(
        #     'Solid finite element system', 'solid'))
        # self.subsections.append(subsection('Solid solver control', 'solid'))
        # self.subsections.append(subsection(
        #     'Solid material properties', 'solid'))
        # self.subsections.append(subsection(
        #     'Solid Dirichlet BCs', 'solid_dirichilet'))
        # self.subsections.append(subsection(
        #     'Solid Neumann BCs', 'solid_neumann'))

    def cache_properties(self):
        for sec in self.subsections:
            sec.cache_properties()

    def write(self, out):
        for sec in self.subsections:
            sec.write(out)
