<?xml version="1.0"?>
<SMTK_AttributeSystem Version="2">
	<Definitions>
		<AttDef Type="fluid" BaseType="" Unique="ture" Associations="">
			<ItemDefinitions>
				<Group Name="fe_system" Label="FE system" AdvanceLevel="0">
					<ItemDefinitions>
						<Int Name="pressure_degree" Label="Pressure Degree" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">1</Min>
							</RangeInfo>
							<DefaultValue>1</DefaultValue>
						</Int>
						<Int Name="velocity_degree" Label="Velocity Degree" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">1</Min>
							</RangeInfo>
							<DefaultValue>1</DefaultValue>
						</Int>
					</ItemDefinitions>
				</Group>
				<Group Name="material_properties" Label="Material Properties" AdvanceLevel="0">
					<ItemDefinitions>
						<Double Name="dynamic_viscosity" Label="Dynamic Viscosity" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
							</RangeInfo>
							<DefaultValue>1.8e-4</DefaultValue>
						</Double>
						<Double Name="density" Label="Density" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
							</RangeInfo>
							<DefaultValue>1.3e-3</DefaultValue>
						</Double>
					</ItemDefinitions>
				</Group>
				<Group Name="solver_control" Label="Solver Control" AdvanceLevel="0">
					<ItemDefinitions>
						<Double Name="grad_div_stabilization" Label="Grad Div Stabilization" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">0</Min>
								<Max Inclusive="true">1</Max>
							</RangeInfo>
							<DefaultValue>0.1</DefaultValue>
						</Double>
						<Int Name="max_newton_iterations" Label="Max Newton Iterations" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">1</Min>
							</RangeInfo>
							<DefaultValue>8</DefaultValue>
						</Int>
						<Double Name="nonlinear_system_tolerance" Label="Nonlinear System Tolerance" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
								<Max Inclusive="false">1</Max>
							</RangeInfo>
							<DefaultValue>1e-6</DefaultValue>
						</Double>
					</ItemDefinitions>
				</Group>
			</ItemDefinitions>
		</AttDef>
		<AttDef Type="fluid_boundary_conditions" Label="Boundary Conditions" BaseType="" Version="0" Unique="true" Abstract="true">
			<AssociationsDef Name="fluid_boundary_associations" Version="0" NumberOfRequiredValues="0" Extensible="true">
				<MembershipMask>edge</MembershipMask>
			</AssociationsDef>
		</AttDef>
		<AttDef Type="dirichlet" Label="Dirichlet" BaseType="fluid_boundary_conditions" Version="0" Unique="true">
			<ItemDefinitions>
				<Double Name="velocity" Label="Velocity" NumberOfRequiredValues="2" AdvanceLevel="0"></Double>
			</ItemDefinitions>
		</AttDef>
		<AttDef Type="neumann" Label="Neumann" BaseType="fluid_boundary_conditions" Version="0" Unique="true">
			<ItemDefinitions>
				<Double Name="pressure" Label="Pressure" NumberOfRequiredValues="1" AdvanceLevel="0"></Double>
			</ItemDefinitions>
		</AttDef>
	</Definitions>
</SMTK_AttributeSystem>