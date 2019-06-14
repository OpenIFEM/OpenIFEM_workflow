<?xml version="1.0" ?>
<SMTK_AttributeResource Version="3">
	<Categories>
		<Cat>Solid</Cat>
		<Cat>Fluid</Cat>
	</Categories>
	
	<Includes>
		<File>internal/templates/simulation.sbt</File>
		<File>internal/templates/fluid.sbt</File>
		<File>internal/templates/solid.sbt</File>
	</Includes>
	<Views>
		<View Type="Group" Name="OpenIFEM" Label="OpenIFEM" TopLevel="true" TabPosition="North" FilterByCategory="false" FilterByAdvanceLevel="false">
			<Views>
				<View Title="Simulation" />
				<View Title="Fluid" />
				<View Title="Solid" />
			</Views>
		</View>
		<!-- Simulation session -->
		<View Type="Group" Title="Simulation" Label="Simulation" Style="Tiled">
			<Views>
				<View Title="Analysis" />
				<View Title="General" />
			</Views>
		</View>
		<View Type="Analysis" Title="Analysis" Label="Analysis" AnalysisAttributeName="analysis" AnalysisAttributeType="analysis">
		</View>
		<View Type="Instanced" Title="General" Label="General">
			<InstancedAttributes>
				<Att Name="simulation" Type="simulation" />
			</InstancedAttributes>
		</View>
		<!-- Fluid session -->
		<View Type="Group" Title="Fluid" Label="Fluid" Style="Tiled">
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
		<View Type="Attribute" Title="Fluid Boundary Conditions" ModelEntityFilter="e">
			<AttributeTypes>
				<Att Name="fluid_boundary_conditions" Type="fluid_boundary_conditions" />
			</AttributeTypes>
		</View>
		<!-- Solid session -->
		<View Type="Group" Title="Solid" Label="Solid" Style="Tiled">
			<Views>
				<View Title="Solid Parameters" />
				<View Title="Solid Boundary Conditions" />
				<View Title="Solid Materials" />
			</Views>
		</View>
		<View Type="Instanced" Title="Solid Parameters" Label="Parameters">
			<InstancedAttributes>
				<Att Name="solid" Type="solid" />
			</InstancedAttributes>
		</View>
		<View Type="Attribute" Title="Solid Boundary Conditions" ModelEntityFilter="e">
			<AttributeTypes>
				<Att Name="solid_boundary_conditions" Type="solid_boundary_conditions" />
			</AttributeTypes>
		</View>
		<View Type="Attribute" Title="Solid Materials" ModelEntityFilter="f">
			<AttributeTypes>
				<Att Name="solid_materials" Type="solid_materials" />
			</AttributeTypes>
		</View>
	</Views>
</SMTK_AttributeResource>