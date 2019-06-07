<?xml version="1.0"?>
<SMTK_AttributeSystem Version="2">
	<Definitions>
		<AttDef Type="simulation" BaseType="" Unique="ture" Associations="">
			<ItemDefinitions>
				<Group Name="simulation_type" Label="Simulation Type" AdvanceLevel="0">
					<ItemDefinitions>
						<Void Name="solid" Label="Solid" Optional="true" IsEnabledByDefault="true"/>
						<Void Name="fluid" Label="Fluid" Optional="true" IsEnabledByDefault="false"/>
					</ItemDefinitions>
				</Group>
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
				<Double Name="gravity" Label="Gravity" NumberOfRequiredValues="2">
					<RangeInfo>
						<Min Inclusive="true">0</Min>
					</RangeInfo>
					<DefaultValue>0</DefaultValue>
				</Double>
			</ItemDefinitions>
		</AttDef>
	</Definitions>
</SMTK_AttributeSystem>