import React, { useState } from 'react';
import styles from './Tabs.module.css';

export interface TabItem {
  /**
   * ID único da aba
   */
  id: string;

  /**
   * Rótulo da aba
   */
  label: string;

  /**
   * Conteúdo da aba
   */
  content: React.ReactNode;

  /**
   * Se true, a aba fica desabilitada
   */
  disabled?: boolean;
}

export interface TabsProps {
  /**
   * Array de abas
   */
  tabs: TabItem[];

  /**
   * ID da aba ativa (controlada externamente)
   */
  activeTabId?: string;

  /**
   * Callback ao mudar de aba
   */
  onTabChange?: (tabId: string) => void;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Tabs para exibir conteúdo abado
 *
 * @example
 * ```tsx
 * <Tabs
 *   tabs={[
 *     { id: 'tab1', label: 'Aba 1', content: <p>Conteúdo 1</p> },
 *     { id: 'tab2', label: 'Aba 2', content: <p>Conteúdo 2</p> }
 *   ]}
 *   onTabChange={(id) => console.log(id)}
 * />
 * ```
 */
export const Tabs: React.FC<TabsProps> = ({
  tabs,
  activeTabId: controlledActiveTabId,
  onTabChange,
  className = '',
}) => {
  const [uncontrolledActiveTabId, setUncontrolledActiveTabId] = useState(
    tabs[0]?.id || ''
  );

  const isControlled = controlledActiveTabId !== undefined;
  const activeTabId = isControlled ? controlledActiveTabId : uncontrolledActiveTabId;

  const handleTabChange = (tabId: string) => {
    if (isControlled) {
      onTabChange?.(tabId);
    } else {
      setUncontrolledActiveTabId(tabId);
    }
  };

  const activeTab = tabs.find((tab) => tab.id === activeTabId);

  return (
    <div className={`${styles.tabs} ${className}`}>
      <div className={styles.tabList} role="tablist">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`${styles.tab} ${
              activeTabId === tab.id ? styles.active : ''
            } ${tab.disabled ? styles.disabled : ''}`}
            onClick={() => !tab.disabled && handleTabChange(tab.id)}
            disabled={tab.disabled}
            role="tab"
            aria-selected={activeTabId === tab.id}
            aria-controls={`panel-${tab.id}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab && (
        <div
          className={styles.tabPanel}
          id={`panel-${activeTab.id}`}
          role="tabpanel"
          aria-labelledby={`tab-${activeTab.id}`}
        >
          {activeTab.content}
        </div>
      )}
    </div>
  );
};

export default Tabs;
