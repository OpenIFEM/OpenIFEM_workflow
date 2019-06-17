<?xml version="1.0" encoding="UTF-8" ?>
<SMTK_AttributeResource Version="3">
    <Definitions>
        <AttDef Type="export" BaseType="operation" Label="Export to OpenIFEM" Version="1">
            <BriefDescription>
                Write OpenIFEM .prm file.
            </BriefDescription>
            <DetailedDescription>
                Using the specified model and simulation attribute resources, this
                operation will write a OpenIFEM input file to the specified location.
            </DetailedDescription>
            <ItemDefinitions>
                <Component Name="solid_model" Label="Solid Model" LockType="DoNotLock">
                    <Accepts>
                        <Resource Name="smtk::model::Resource" Filter="model" />
                    </Accepts>
                </Component>
                <Component Name="fluid_model" Label="Fluid Model" LockType="DoNotLock">
                    <Accepts>
                        <Resource Name="smtk::model::Resource" Filter="model" />
                    </Accepts>
                </Component>
                <Resource Name="attributes" Label="Attributes" LockType="DoNotLock">
                    <Accepts>
                        <Resource Name="smtk::attribute::Resource" />
                    </Accepts>
                </Resource>
                <File Name="parameters_file" Label="Parameters File" FileFilters="OpenIFEM parameters files (*.prm);;All files (*.*)" Version="0">
                    <BriefDescription>Parameters file to be generated</BriefDescription>
                </File>
            </ItemDefinitions>
        </AttDef>
    </Definitions>
    <Views>
        <View Type="Instanced" Title="Export Settings" TopLevel="true" FilterByCategory="false" FilterByAdvanceLevel="true">
            <InstancedAttributes>
                <Att Name="Options" Type="export" />
            </InstancedAttributes>
        </View>
    </Views>
</SMTK_AttributeResource>