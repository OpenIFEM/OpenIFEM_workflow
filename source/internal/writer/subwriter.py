import os
import sys
from abc import ABCMeta, abstractmethod
import smtk
import smtk.attribute


class property:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def write(self, out):
        # Write sotred property
        out.write('\nset  {} = {}\n'.format(self.name, self.value))


class subsection:
    def __init__(self, title, sim_atts):
        self.title = title
        self.sim_atts = sim_atts
        self.properties = list()

    @abstractmethod
    def cache_properties(self):
        pass

    def generate_regular_property(self, item_path, parent_att):
        print('Reading {}...\n'.format(item_path))
        item = parent_att.itemAtPath(item_path, '/')
        if item is None:
            print('Skip item {}\n'.format(item_path))
            return
        # Look for number of values
        n_values = item.numberOfValues()
        if not n_values:
            return
        string_to_write = str(item.value(0))
        if n_values > 1:
            for i in range(1, n_values):
                string_to_write += (', {}'.format(item.value(i)))
        self.properties.append(property(item.label(), string_to_write))

    def write(self, out):
        # Write subsection header first
        out.write('\nsubsection {}\n'.format(self.title))
        # Iterate over member properties
        for p in self.properties:
            p.write(out)
        # End subsection
        out.write('\nend\n')


class entity_subsection(subsection):
    def __init__(self, title, sim_atts, sim_model):
        subsection.__init__(self, title, sim_atts)
        self.sim_model = sim_model


class simulation_subsection(subsection):
    def cache_properties(self):
        # Find analysis
        analysis_att = self.sim_atts.findAttribute('analysis')
        if not analysis_att:
            raise RuntimeError('Internal Error -- missing analysis att')
        solid_analysis = 0x1
        fluid_analysis = 0x2
        self.analysis = 0x0
        self.analysis |= (solid_analysis * analysis_att.findVoid('Solid').isEnabled()
                          ) | (fluid_analysis * analysis_att.findVoid('Fluid').isEnabled())
        # Determine whether it is a FSI, Solid or Fluid simulation
        if ((self.analysis & solid_analysis) and (self.analysis & fluid_analysis)):
            self.properties.append(property('Simulation type', 'FSI'))
        elif (self.analysis & solid_analysis):
            self.properties.append(property('Simulation type', 'Solid'))
        elif (self.analysis & fluid_analysis):
            self.properties.append(property('Simulation type', 'Fluid'))
        '''
        '''
        # Get simulation parameters attribute
        simulation_att = self.sim_atts.findAttribute('simulation')
        # Dimension
        self.generate_regular_property('dimension', simulation_att)
        # Global refinements
        self.generate_regular_property('global_refinements', simulation_att)
        # End time
        self.generate_regular_property('end_time', simulation_att)
        # Time step size
        self.generate_regular_property('time_step_size', simulation_att)
        # Output interval
        self.generate_regular_property('output_interval', simulation_att)
        # Refinement interval
        self.generate_regular_property('refinement_interval', simulation_att)
        # Save interval
        self.generate_regular_property('save_interval', simulation_att)
        # Gravity
        self.generate_regular_property('gravity', simulation_att)


class fluid_FE_subsection(subsection):
    def cache_properties(self):
        # Get fluid parameters attribute
        fluid_att = self.sim_atts.findAttribute('fluid')
        # Pressure degree
        self.generate_regular_property('fe_system/pressure_degree', fluid_att)
        # Velocity degree
        self.generate_regular_property('fe_system/velocity_degree', fluid_att)


class fluid_material_subsection(subsection):
    def cache_properties(self):
        # Get fluid parameters attribute
        fluid_att = self.sim_atts.findAttribute('fluid')
        # Dynamic viscosity
        self.generate_regular_property(
            'material_properties/dynamic_viscosity', fluid_att)
        # Density
        self.generate_regular_property(
            'material_properties/fluid_density', fluid_att)


class fluid_sc_subsection(subsection):
    def cache_properties(self):
        # Get fluid parameters attribute
        fluid_att = self.sim_atts.findAttribute('fluid')
        # Grad-Div stabilization
        self.generate_regular_property(
            'solver_control/grad_div_stabilization', fluid_att)
        # Max Newton iterations
        self.generate_regular_property(
            'solver_control/max_newton_iterations', fluid_att)
        # Nonlinear system tolerance
        self.generate_regular_property(
            'solver_control/nonlinear_system_tolerance', fluid_att)


class fluid_dirichlet_subsection(entity_subsection):
    def cache_properties(self):
        # Values to write
        n_bcs = int(0)
        bc_ids = list()
        bc_components = list()
        bc_values = str()
        x_component = 0x1
        y_component = 0x2
        # Every BC is an individual attribute, need to put them in a list
        fluid_bc_atts = self.sim_atts.findAttributes(
            'fluid_dirichlet')
        for bc_att in fluid_bc_atts:
            # Here sub_n_bcs is the number of boundaries
            # assigned to this BC
            sub_n_bcs = int(0)
            # Find eneity UUID associated with this BC att
            sub_bc_uuids = bc_att.associatedModelEntityIds()
            # Convert them into integer
            for uuid in sub_bc_uuids:
                idlist = self.sim_model.integerProperty(uuid, 'pedigree id')
                # Put into bc_ids list.
                sub_n_bcs += 1
                bc_ids.append(idlist[0])
            n_bcs += sub_n_bcs
            # Get the components and values
            item_x = bc_att.itemAtPath('velocity/x', '/')
            item_y = bc_att.itemAtPath('velocity/y', '/')
            components = 0x0
            components |= x_component * item_x.isEnabled() | y_component * \
                item_y.isEnabled()
            # Add component mask to bc_component
            bc_components.extend([components for i in range(sub_n_bcs)])
            # Get the values
            values = list()
            if (components & x_component):
                values.append(item_x.value(0))
            if (components & y_component):
                values.append(item_y.value(0))
            # Add values
            for j in range(sub_n_bcs):
                bc_values += " ".join("{}, ".format(i) for i in values)
        # Add properties
        self.properties.append(property('Number of Dirichlet BCs', n_bcs))
        string_ids = " ".join("{}, ".format(i) for i in bc_ids)
        string_ids = string_ids[:-2]
        self.properties.append(property('Dirichlet boundary id', string_ids))
        string_components = " ".join("{}, ".format(i) for i in bc_components)
        string_components = string_components[:-2]
        string_components = "3" if not string_components else string_components
        self.properties.append(
            property('Dirichlet boundary components', string_components))
        bc_values = bc_values[:-2]
        self.properties.append(
            property('Dirichlet boundary values', bc_values))


class fluid_neumann_subsection(entity_subsection):
    def cache_properties(self):
        # Values to write
        n_bcs = int(0)
        bc_ids = list()
        bc_values = str()
        # Every BC is an individual attribute, need to put them in a list
        fluid_bc_atts = self.sim_atts.findAttributes(
            'fluid_neumann')
        for bc_att in fluid_bc_atts:
            # Here sub_n_bcs is the number of boundaries
            # assigned to this BC
            sub_n_bcs = int(0)
            # Find eneity UUID associated with this BC att
            sub_bc_uuids = bc_att.associatedModelEntityIds()
            # Convert them into integer
            for uuid in sub_bc_uuids:
                idlist = self.sim_model.integerProperty(uuid, 'pedigree id')
                # Put into bc_ids list.
                sub_n_bcs += 1
                bc_ids.append(idlist[0])
            item = bc_att.itemAtPath('pressure', '/')
            n_bcs += sub_n_bcs
            value = item.value(0)
            bc_values += "{}, ".format(value)
        # Add properties
        self.properties.append(property('Number of Neumann BCs', n_bcs))
        string_ids = " ".join("{}, ".format(i) for i in bc_ids)
        string_ids = string_ids[:-2]
        string_ids = "0" if not string_ids else string_ids
        self.properties.append(property('Neumann boundary id', string_ids))
        bc_values = bc_values[:-2]
        bc_values = "0" if not bc_values else bc_values
        self.properties.append(
            property('Neumann boundary values', bc_values))


class solid_FE_subsection(subsection):
    def cache_properties(self):
        # Get solid parameters attribute
        solid_att = self.sim_atts.findAttribute('solid')
        # Solid degree
        self.generate_regular_property('fe_system/degree', solid_att)


class solid_material_subsecion(entity_subsection):
    def cache_properties(self):
        # Write solid type first
        solid_att = self.sim_atts.findAttribute('solid')
        self.generate_regular_property(
            'material_properties/solid_type', solid_att)
        # Values to write
        E_moduli = list()
        nu = list()
        C_properties = list()
        # Every material is an individual attribute, need to pu them in a list
        solid_material_atts = self.sim_atts.findAttributes('solid_materials')
        n_parts = len(solid_material_atts)
        n_parts = 1 if not n_parts else n_parts
        # For now, we do not care entity IDs associated with the material
        # because OpenIFEM assumes that material ID starts from 1 and each ID
        # must have a separated material
        for mat_att in solid_material_atts:
            E_moduli.append(mat_att.itemAtPath('youngs_modulus', '/').value(0))
            nu.append(mat_att.itemAtPath('poissons_ratio', '/').value(0))
            C_properties.append(mat_att.itemAtPath(
                'hyper_elastic_parameters/C1', '/').value(0))
            C_properties.append(mat_att.itemAtPath(
                'hyper_elastic_parameters/bulk_modulus', '/').value(0))
        # Add properties
        self.properties.append(property('Number of solid parts', n_parts))
        self.generate_regular_property(
            'material_properties/solid_density', solid_att)
        string_youngs = " ".join("{}, ".format(i) for i in E_moduli)
        string_youngs = string_youngs[:-2]
        string_youngs = "0" if not string_youngs else string_youngs
        self.properties.append(property('Young\'s modulus', string_youngs))
        string_nu = " ".join("{}, ".format(i) for i in nu)
        string_nu = string_nu[:-2]
        string_nu = "0" if not string_nu else string_nu
        self.properties.append(property('Poisson\'s ratio', string_nu))
        string_C = " ".join("{}, ".format(i) for i in C_properties)
        string_C = string_C[:-2]
        string_C = "0" if not string_C else string_C
        self.properties.append(property('Hyperelastic parameters', string_C))


class solid_sc_subsection(subsection):
    def cache_properties(self):
        # Get solid parameters attribute
        solid_att = self.sim_atts.findAttribute('solid')
        # Damping
        self.generate_regular_property(
            'solver_control/damping', solid_att)
        # Max Newton iterations
        self.generate_regular_property(
            'solver_control/max_newton_iterations', solid_att)
        # Displacement tolerance
        self.generate_regular_property(
            'solver_control/displacement_tolerance', solid_att)
        # Force tolerance
        self.generate_regular_property(
            'solver_control/force_tolerance', solid_att)


class solid_dirichlet_subsection(entity_subsection):
    def cache_properties(self):
        # Values to write
        n_bcs = int(0)
        bc_ids = list()
        bc_components = list()
        x_component = 0x1
        y_component = 0x2
        # Every BC is an individual attribute, need to put them in a list
        solid_bc_atts = self.sim_atts.findAttributes(
            'solid_dirichlet')
        for bc_att in solid_bc_atts:
            # Here sub_n_bcs is the number of boundaries
            # assigned to this BC
            sub_n_bcs = int(0)
            # Find eneity UUID associated with this BC att
            sub_bc_uuids = bc_att.associatedModelEntityIds()
            # Convert them into integer
            for uuid in sub_bc_uuids:
                idlist = self.sim_model.integerProperty(uuid, 'pedigree id')
                # Put into bc_ids list.
                sub_n_bcs += 1
                bc_ids.append(idlist[0])
            n_bcs += sub_n_bcs
            # Get the components and values
            item_x = bc_att.itemAtPath('x', '/')
            item_y = bc_att.itemAtPath('y', '/')
            components = 0x0
            components |= x_component * item_x.isEnabled() | y_component * \
                item_y.isEnabled()
            # Add component mask to bc_component
            bc_components.extend([components for i in range(sub_n_bcs)])
        # Add properties
        self.properties.append(property('Number of Dirichlet BCs', n_bcs))
        string_ids = " ".join("{}, ".format(i) for i in bc_ids)
        string_ids = string_ids[:-2]
        string_ids = '0' if not string_ids else string_ids
        self.properties.append(property('Dirichlet boundary id', string_ids))
        string_components = " ".join("{}, ".format(i) for i in bc_components)
        string_components = string_components[:-2]
        string_components = '3' if not string_components else string_components
        self.properties.append(
            property('Dirichlet boundary components', string_components))


class solid_neumann_subsection(entity_subsection):
    def cache_properties(self):
        # Values to write
        n_bcs = int(0)
        bc_ids = list()
        bc_values = str()
        # Every BC is an individual attribute, need to put them in a list
        solid_bc_atts = self.sim_atts.findAttributes(
            'solid_neumann')
        for bc_att in solid_bc_atts:
            # Here sub_n_bcs is the number of boundaries
            # assigned to this BC
            sub_n_bcs = int(0)
            # Find eneity UUID associated with this BC att
            sub_bc_uuids = bc_att.associatedModelEntityIds()
            # Convert them into integer
            for uuid in sub_bc_uuids:
                idlist = self.sim_model.integerProperty(uuid, 'pedigree id')
                # Put into bc_ids list.
                sub_n_bcs += 1
                bc_ids.append(idlist[0])
            item = bc_att.itemAtPath('Traction', '/')
            n_bcs += sub_n_bcs
            value = [item.value(0), item.value(1)]
            bc_values += "{}, {}, ".format(value[0], value[1])
        # Add properties
        self.properties.append(property('Number of Neumann BCs', n_bcs))
        string_ids = " ".join("{}, ".format(i) for i in bc_ids)
        string_ids = string_ids[:-2]
        string_ids = "0" if not string_ids else string_ids
        self.properties.append(property('Neumann boundary id', string_ids))
        # Only support traction right now
        self.properties.append(property('Neumann boundary type', 'Traction'))
        bc_values = bc_values[:-2]
        bc_values = "0, 0" if not bc_values else bc_values
        self.properties.append(
            property('Neumann boundary values', bc_values))
