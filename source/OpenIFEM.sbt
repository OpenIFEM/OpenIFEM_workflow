<?xml version="1.0"?>
<SMTK_AttributeSystem Version="2">
	<Includes>
		<File>internal/templates/simulation.sbt</File>
		<File>internal/templates/fluid.sbt</File>
	</Includes>
	<Views>
		<View Type="Group" Name="OpenIFEM" Label="OpenIFEM" TopLevel="true" TabPosition="North" FilterByCategory="false" FilterByAdvanceLevel="false">
			<Views>
				<View Title="Simulation" />
				<View Title="Fluid" />
			</Views>
		</View>
		<View Type="Instanced" Title="Simulation" Label="Simulation">
			<InstancedAttributes>
				<Att Name="simulation" Type="simulation" />
			</InstancedAttributes>
		</View>
		<View Type="Group" Title="Fluid" Label="Fluid" TabPosition="North">
			<Views>
				<View Title="Fluid parameters" />
				<View Title="Fluid Boundary Conditions" />
			</Views>
		</View>
		<View Type="Instanced" Title="Fluid parameters" Label="Parameters">
			<InstancedAttributes>
				<Att Name="fluid" Type="fluid" />
			</InstancedAttributes>
		</View>
		<View Type="ModelEntity" Title="Fluid Boundary Conditions" ModelEntityFilter="e">
			<AttributeTypes>
				<Att Name="fluid_boundary_conditions" Type="fluid_boundary_conditions" />
			</AttributeTypes>
		</View>
	</Views>
</SMTK_AttributeSystem>