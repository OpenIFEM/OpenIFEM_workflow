<?xml version="1.0" ?>
<SMTK_AttributeResource Version="3">
	<Categories>
		<Cat>Fluid</Cat>
		<Cat>Solid</Cat>
	</Categories>
	
	<Analyses>
		<Analysis Type="Fluid">
			<Cat>Fluid</Cat>
		</Analysis>
		<Analysis Type="Solid">
			<Cat>Solid</Cat>
		</Analysis>
	</Analyses>
	
	<Definitions>
		<AttDef Type="simulation" BaseType="" Unique="ture" Associations="">
			<ItemDefinitions>
				<Int Name="dimension" Label="Dimension" NumberOfRequiredValues="1">
					<DiscreteInfo DefaultIndex="0">
						<Value Enum="2">2</Value>
						<Value Enum="3">3</Value>
					</DiscreteInfo>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Int>
				<Int Name="global_refinements" Label="Global refinements" NumberOfRequiredValues="2">
					<RangeInfo>
						<Min Inclusive="true">0</Min>
					</RangeInfo>
					<DefaultValue>0</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Int>
				<Double Name="end_time" Label="End time" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>1</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Double Name="time_step_size" Label="Time step size" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>1e-2</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Double Name="output_interval" Label="Output interval" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>1e-2</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Double Name="refinement_interval" Label="Refinement interval" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>10</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Double Name="save_interval" Label="Save interval" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>10</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
				<Double Name="gravity" Label="Gravity" NumberOfRequiredValues="2">
					<RangeInfo>
						<Min Inclusive="true">0</Min>
					</RangeInfo>
					<DefaultValue>0</DefaultValue>
					<Categories>
						<Cat>Fluid</Cat>
						<Cat>Solid</Cat>
					</Categories>
				</Double>
			</ItemDefinitions>
		</AttDef>
	</Definitions>
</SMTK_AttributeResource>