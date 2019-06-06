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
				<Att Name="simulation-instance" Type="simulation" />
			</InstancedAttributes>
		</View>
		<View Type="Instanced" Title="Fluid" Label="Fluid">
			<InstancedAttributes>
				<Att Name="fluid-instance" Type="fluid" />
			</InstancedAttributes>
		</View>
	</Views>
</SMTK_AttributeSystem>