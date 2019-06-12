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
        # Look for number of values
        n_values = item.numberOfValues()
        if (not n_values):
            return
        string_to_write = str(item.value(0))
        if (n_values > 1):
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
        # Get simulation parameters attribute
        fluid_att = self.sim_atts.findAttribute('fluid')
        # Pressure degree
        self.generate_regular_property('fe_system/pressure_degree', fluid_att)
        # Velocity degree
        self.generate_regular_property('fe_system/velocity_degree', fluid_att)


class fluid_material_subsection(subsection):
    def cache_properties(self):
        # Get simulation parameters attribute
        fluid_att = self.sim_atts.findAttribute('fluid')
        # Dynamic viscosity
        self.generate_regular_property(
            'material_properties/dynamic_viscosity', fluid_att)
        # Density
        self.generate_regular_property(
            'material_properties/fluid_density', fluid_att)


class fluid_sc_subsection(subsection):
    def cache_properties(self):
        # Get simulation parameters attribute
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
