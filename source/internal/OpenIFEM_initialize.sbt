<?xml version="1.0" encoding="UTF-8" ?>
<SMTK_AttributeResource Version="3">
    <Definitions>
        <AttDef Type="initialize" BaseType="operation" Label="Initialize OpenIFEM" Version="1">
            <BriefDescription>
                Create OpenIFEM workspace.
            </BriefDescription>
            <DetailedDescription>
                Specify attribute, simulation type, dimensions and fluid/solid models, and initialize
                the workspace for OpenIFEM.
            </DetailedDescription>
            <ItemDefinitions>
                <Int Name="dimension" Label="Dimension">
                    <DiscreteInfo DefaultIndex="0">
                        <Value Enum="2">2</Value>
                        <Value Enum="3">3</Value>
                    </DiscreteInfo>
                </Int>
                <File Name="solid_model" Label="Solid Model" FileFilters="Gmsh mesh files (*.msh);;All files (*,*)" Version="0" Optional="true" IsEnabledByDefault="false"></File>
                <File Name="fluid_model" Label="Fluid Model" FileFilters="Gmsh mesh files (*.msh);;All files (*,*)" Version="0" Optional="true" IsEnabledByDefault="false"></File>
            </ItemDefinitions>
        </AttDef>
        <!-- Result -->
        <include href="smtk/operation/Result.xml" />
        <AttDef Type="result(openIFEM)" BaseType="result">
            <ItemDefinitions>
                <!-- The model imported from the file. -->
                <Resource Name="resource" HoldReference="true" Extensible="true">
                    <Accepts>
                        <Resource Name="smtk::session::mesh::Resource" />
                        <Resource Name="smtk::attribute::Resource" />
                    </Accepts>
                </Resource>
                
                <Component Name="model" Extensible="true">
                    <Accepts>
                        <Resource Name="smtk::session::mesh::Resource" Filter="" />
                    </Accepts>
                </Component>
                
                <Component Name="mesh_created" Extensible="true">
                    <Accepts>
                        <Resource Name="smtk::session::mesh::Resource" Filter="" />
                    </Accepts>
                </Component>
                <Void Name="allow camera reset" IsEnabledByDefault="true" AdvanceLevel="11" />
                
            </ItemDefinitions>
        </AttDef>
    </Definitions>
</SMTK_AttributeResource>