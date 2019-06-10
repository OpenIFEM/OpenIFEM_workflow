<?xml version="1.0"?>
<SMTK_AttributeResource Version="3">
	<Categories>
		<Cat>Solid</Cat>
	</Categories>

	<Definitions>
		<!-- parameters -->
		<AttDef Type="solid" BaseType="" Unique="ture" Associations="">
			<ItemDefinitions>
				<Group Name="fe_system" Label="FE system" AdvanceLevel="0">
					<ItemDefinitions>
						<Int Name="degree" Label="Degree" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">1</Min>
							</RangeInfo>
							<DefaultValue>1</DefaultValue>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Int>
					</ItemDefinitions>
				</Group>
				<Group Name="material_properties" Label="Material Properties" AdvanceLevel="0">
					<ItemDefinitions>
						<String Name="solid_type" Label="Solid Type" NumberOfRequiredValues="1">
							<DiscreteInfo DefaultIndex="0">
								<Value Enum="LinearElastic">LinearElastic</Value>
								<Value Enum="NeoHookean">NeoHookean</Value>
							</DiscreteInfo>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</String>
						<Double Name="global_density" Label="Global Density">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
							</RangeInfo>
							<DefaultValue>1</DefaultValue>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Double>
					</ItemDefinitions>
				</Group>
				<Group Name="solver_control" Label="Solver Control" AdvanceLevel="0">
					<ItemDefinitions>
						<Double Name="damping" Label="Damping" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">0</Min>
							</RangeInfo>
							<DefaultValue>0</DefaultValue>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Double>
						<Int Name="max_newton_iterations" Label="Max Newton Iterations" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="true">1</Min>
							</RangeInfo>
							<DefaultValue>10</DefaultValue>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Int>
						<Double Name="displacement_tolerance" Label="Displacement Tolerance" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
								<Max Inclusive="false">1</Max>
							</RangeInfo>
							<DefaultValue>1e-6</DefaultValue>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Double>
						<Double Name="force_tolerance" Label="Force Tolerance" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
								<Max Inclusive="false">1</Max>
							</RangeInfo>
							<DefaultValue>1e-6</DefaultValue>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Double>
					</ItemDefinitions>
				</Group>
			</ItemDefinitions>
		</AttDef>
		<!-- boundary conditions -->
		<AttDef Type="solid_boundary_conditions" Label="Boundary Conditions" BaseType="" Version="0" Unique="true" Abstract="true">
			<AssociationsDef Name="solid_boundary_associations" Version="0" NumberOfRequiredValues="0" Extensible="true">
				<MembershipMask>edge</MembershipMask>
			</AssociationsDef>
		</AttDef>
		<AttDef Type="solid_dirichilet" Label="Dirichlet (Fixed)" BaseType="solid_boundary_conditions" Version="0" Unique="true">
			<ItemDefinitions>
				<Group Name="directions" Label="Directions" AdvanceLevel="0">
					<ItemDefinitions>
						<Void Name="x" label="x" Optional="true" IsEnabledByDefault="false">
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Void>
						<Void Name="y" label="y" Optional="true" IsEnabledByDefault="false">
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Void>
					</ItemDefinitions>
				</Group>
			</ItemDefinitions>
		</AttDef>
		<AttDef Type="solid_neumann" Label="Traction" BaseType="solid_boundary_conditions" Version="0" Unique="true">
			<ItemDefinitions>
				<Double Name="Traction" Label="Traction" NumberOfRequiredValues="2" AdvanceLevel="0">
					<ComponentLabels>
						<Label>x</Label>
						<Label>y</Label>
					</ComponentLabels>
					<DefaultValue>0</DefaultValue>
					<Categories>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
			</ItemDefinitions>
		</AttDef>
		<!-- materials -->
		<AttDef Type="solid_materials" Label="Solid Materials" BaseType="" Unique="true" Version="0">
			<AssociationsDef Name="solid_material_associations" Version="0" NumberOfRequiredValues="0" Extensible="true">
				<MembershipMask>face</MembershipMask>
			</AssociationsDef>
			<ItemDefinitions>
				<Double Name="youngs_modulus" Label="Young's Modulus" Version="0">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<Categories>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Double Name="poissons_ratio" Label="Poisson's Ratio" Version="0">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
						<Max Inclusive="false">0.5</Max>
					</RangeInfo>
					<DefaultValue>0.3</DefaultValue>
					<Categories>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Group Name="hyper_elastic_parameters" Label="Hyperelastic Parameters" AdvanceLevel="0">
					<ItemDefinitions>
						<Double Name="shear_modulus" Label="Shear Modulus" Version="0" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
							</RangeInfo>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Double>
						<Double Name="bulk_modulus" Label="Bulk Modulus" Version="0" NumberOfRequiredValues="1">
							<RangeInfo>
								<Min Inclusive="false">0</Min>
							</RangeInfo>
							<Categories>
								<Cat>Solid</Cat>
							</Categories>
						</Double>
					</ItemDefinitions>
				</Group>
			</ItemDefinitions>
		</AttDef>
	</Definitions>
</SMTK_AttributeResource>
