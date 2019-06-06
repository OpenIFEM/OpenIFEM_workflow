<?xml version="1.0"?>
<SMTK_AttributeSystem Version="2">
	<Definitions>
		<AttDef Type="simulation" BaseType="" Unique="ture" Associations="">
			<ItemDefinitions>
				<String Name="simulation_type" Label="Simulation Type" NumberOfRequiredValues="1">
					<DiscreteInfo DefaultIndex="0">
						<Value Enum="Solid">Solid</Value>
						<Value Enum="Fluid">Fluid</Value>
						<Value Enum="FSI">FSI</Value>
					</DiscreteInfo>
				</String>
				<Int Name="dimensions" Label="Dimensions" NumberOfRequiredValues="1">
					<DiscreteInfo DefaultIndex="0">
						<Value Enum="2">2</Value>
						<Value Enum="3">3</Value>
					</DiscreteInfo>
				</Int>
				<Int Name="global_refinements" Label="Global Refinements" NumberOfRequiredValues="2">
					<RangeInfo>
						<Min Inclusive="true">0</Min>
					</RangeInfo>
					<DefaultValue>0</DefaultValue>
				</Int>
				<Double Name="end_time" Label="End Time" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>1</DefaultValue>
				</Double>
				<Double Name="time_step_size" Label="Time Step Size" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>1e-2</DefaultValue>
				</Double>
				<Double Name="output_interval" Label="Output Interval" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>1e-2</DefaultValue>
				</Double>
				<Double Name="refinement_interval" Label="Refinement Interval" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>10</DefaultValue>
				</Double>
				<Double Name="Save_interval" Label="Save Interval" NumberOfRequiredValues="1">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
					<DefaultValue>10</DefaultValue>
				</Double>
				<Double Name="gravity" Label="Gravity" NumberOfRequiredValues="3">
					<RangeInfo>
						<Min Inclusive="false">0</Min>
					</RangeInfo>
				</Double>
			</ItemDefinitions>
		</AttDef>
	</Definitions>
</SMTK_AttributeSystem>