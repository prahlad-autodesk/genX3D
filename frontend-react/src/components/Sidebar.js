import React, { useState } from 'react';
import styled from 'styled-components';
import { 
  Layers, 
  ChevronRight, 
  ChevronDown,
  Trash2,
  Copy
} from 'lucide-react';

const SidebarContainer = styled.div`
  width: 280px;
  background: #2a2a2a;
  border-right: 1px solid #444;
  display: flex;
  flex-direction: column;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
`;

const SidebarHeader = styled.div`
  background: #333;
  color: white;
  padding: 16px;
  border-bottom: 1px solid #444;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SidebarSection = styled.div`
  border-bottom: 1px solid #444;
`;

const SectionHeader = styled.div`
  background: #333;
  color: white;
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  font-weight: 500;

  &:hover {
    background: #3a3a3a;
  }
`;

const SectionContent = styled.div`
  padding: 12px 16px;
  background: #1a1a1a;
`;

const ModelItem = styled.div`
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 8px 12px;
  margin-bottom: 8px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;

  &:hover {
    background: #3a3a3a;
    border-color: #666;
  }

  &.active {
    border-color: #4CAF50;
    background: #2d4a2d;
  }
`;

const ModelActions = styled.div`
  display: flex;
  gap: 4px;
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 2px;
  border-radius: 2px;

  &:hover {
    color: white;
    background: #444;
  }
`;

const PropertyItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
  font-size: 12px;
  border-bottom: 1px solid #333;

  &:last-child {
    border-bottom: none;
  }
`;

const PropertyLabel = styled.span`
  color: #888;
`;

const PropertyValue = styled.span`
  color: white;
  font-weight: 500;
`;

const Input = styled.input`
  background: #333;
  border: 1px solid #555;
  color: white;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 12px;
  font-family: inherit;
  width: 80px;

  &:focus {
    outline: none;
    border-color: #4CAF50;
  }
`;

const Sidebar = () => {
  const [expandedSections, setExpandedSections] = useState({
    models: true,
    properties: true,
    settings: false
  });

  const [selectedModel, setSelectedModel] = useState('model_1');
  const [models] = useState([
    { id: 'model_1', name: 'Sphere', type: 'sphere', visible: true },
    { id: 'model_2', name: 'Cylinder', type: 'cylinder', visible: true },
    { id: 'model_3', name: 'Box', type: 'box', visible: false }
  ]);

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const handleModelSelect = (modelId) => {
    setSelectedModel(modelId);
  };

  const handleModelToggle = (modelId) => {
    console.log(`Toggle visibility for model: ${modelId}`);
  };

  const handleModelDelete = (modelId) => {
    console.log(`Delete model: ${modelId}`);
  };

  const handleModelDuplicate = (modelId) => {
    console.log(`Duplicate model: ${modelId}`);
  };

  const selectedModelData = models.find(m => m.id === selectedModel);

  return (
    <SidebarContainer>
      <SidebarHeader>
        <Layers size={16} />
        Model Explorer
      </SidebarHeader>

      {/* Models Section */}
      <SidebarSection>
        <SectionHeader onClick={() => toggleSection('models')}>
          Models ({models.length})
          {expandedSections.models ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        </SectionHeader>
        {expandedSections.models && (
          <SectionContent>
            {models.map(model => (
              <ModelItem
                key={model.id}
                className={selectedModel === model.id ? 'active' : ''}
                onClick={() => handleModelSelect(model.id)}
              >
                <div>
                  <div style={{ fontWeight: '500' }}>{model.name}</div>
                  <div style={{ fontSize: '10px', color: '#888' }}>{model.type}</div>
                </div>
                <ModelActions>
                  <ActionButton
                    onClick={(e) => {
                      e.stopPropagation();
                      handleModelToggle(model.id);
                    }}
                    title="Toggle visibility"
                  >
                    <Layers size={12} />
                  </ActionButton>
                  <ActionButton
                    onClick={(e) => {
                      e.stopPropagation();
                      handleModelDuplicate(model.id);
                    }}
                    title="Duplicate"
                  >
                    <Copy size={12} />
                  </ActionButton>
                  <ActionButton
                    onClick={(e) => {
                      e.stopPropagation();
                      handleModelDelete(model.id);
                    }}
                    title="Delete"
                  >
                    <Trash2 size={12} />
                  </ActionButton>
                </ModelActions>
              </ModelItem>
            ))}
          </SectionContent>
        )}
      </SidebarSection>

      {/* Properties Section */}
      <SidebarSection>
        <SectionHeader onClick={() => toggleSection('properties')}>
          Properties
          {expandedSections.properties ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        </SectionHeader>
        {expandedSections.properties && selectedModelData && (
          <SectionContent>
            <PropertyItem>
              <PropertyLabel>Name:</PropertyLabel>
              <PropertyValue>{selectedModelData.name}</PropertyValue>
            </PropertyItem>
            <PropertyItem>
              <PropertyLabel>Type:</PropertyLabel>
              <PropertyValue>{selectedModelData.type}</PropertyValue>
            </PropertyItem>
            <PropertyItem>
              <PropertyLabel>Visible:</PropertyLabel>
              <PropertyValue>{selectedModelData.visible ? 'Yes' : 'No'}</PropertyValue>
            </PropertyItem>
            
            {selectedModelData.type === 'sphere' && (
              <>
                <PropertyItem>
                  <PropertyLabel>Radius:</PropertyLabel>
                  <Input type="number" defaultValue="5" step="0.1" />
                </PropertyItem>
              </>
            )}
            
            {selectedModelData.type === 'cylinder' && (
              <>
                <PropertyItem>
                  <PropertyLabel>Radius:</PropertyLabel>
                  <Input type="number" defaultValue="3" step="0.1" />
                </PropertyItem>
                <PropertyItem>
                  <PropertyLabel>Height:</PropertyLabel>
                  <Input type="number" defaultValue="10" step="0.1" />
                </PropertyItem>
              </>
            )}
            
            {selectedModelData.type === 'box' && (
              <>
                <PropertyItem>
                  <PropertyLabel>Width:</PropertyLabel>
                  <Input type="number" defaultValue="10" step="0.1" />
                </PropertyItem>
                <PropertyItem>
                  <PropertyLabel>Length:</PropertyLabel>
                  <Input type="number" defaultValue="5" step="0.1" />
                </PropertyItem>
                <PropertyItem>
                  <PropertyLabel>Height:</PropertyLabel>
                  <Input type="number" defaultValue="3" step="0.1" />
                </PropertyItem>
              </>
            )}
          </SectionContent>
        )}
      </SidebarSection>

      {/* Settings Section */}
      <SidebarSection>
        <SectionHeader onClick={() => toggleSection('settings')}>
          Settings
          {expandedSections.settings ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        </SectionHeader>
        {expandedSections.settings && (
          <SectionContent>
            <PropertyItem>
              <PropertyLabel>Grid Size:</PropertyLabel>
              <Input type="number" defaultValue="1" step="0.1" />
            </PropertyItem>
            <PropertyItem>
              <PropertyLabel>Snap to Grid:</PropertyLabel>
              <PropertyValue>Enabled</PropertyValue>
            </PropertyItem>
            <PropertyItem>
              <PropertyLabel>Auto Save:</PropertyLabel>
              <PropertyValue>Every 5 min</PropertyValue>
            </PropertyItem>
          </SectionContent>
        )}
      </SidebarSection>
    </SidebarContainer>
  );
};

export default Sidebar; 