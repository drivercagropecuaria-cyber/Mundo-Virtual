import React, { useState, useRef, useEffect } from 'react';
import styles from './Dropdown.module.css';

export interface DropdownOption {
  /**
   * Identificador único da opção
   */
  id: string | number;

  /**
   * Rótulo a exibir
   */
  label: string;

  /**
   * Se true, a opção fica desabilitada
   */
  disabled?: boolean;
}

export interface DropdownProps {
  /**
   * Opções do dropdown
   */
  options: DropdownOption[];

  /**
   * ID da opção selecionada
   */
  selectedId?: string | number;

  /**
   * Callback ao selecionar uma opção
   */
  onChange: (optionId: string | number) => void;

  /**
   * Placeholder quando nada está selecionado
   */
  placeholder?: string;

  /**
   * Label do dropdown
   */
  label?: string;

  /**
   * Se true, permite busca/filtro
   */
  searchable?: boolean;

  /**
   * Se true, fica desabilitado
   */
  disabled?: boolean;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Dropdown/Select reutilizável
 *
 * @example
 * ```tsx
 * <Dropdown
 *   label="Categoria"
 *   options={[
 *     { id: '1', label: 'Opção 1' },
 *     { id: '2', label: 'Opção 2' }
 *   ]}
 *   onChange={(id) => console.log(id)}
 *   searchable
 * />
 * ```
 */
export const Dropdown: React.FC<DropdownProps> = ({
  options,
  selectedId,
  onChange,
  placeholder = 'Selecione uma opção',
  label,
  searchable = false,
  disabled = false,
  className = '',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  const selectedOption = options.find((opt) => opt.id === selectedId);
  const filteredOptions = searchable
    ? options.filter((opt) =>
        opt.label.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : options;

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      searchInputRef.current?.focus();
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleSelect = (optionId: string | number) => {
    onChange(optionId);
    setIsOpen(false);
    setSearchTerm('');
  };

  return (
    <div ref={containerRef} className={`${styles.container} ${className}`}>
      {label && <label className={styles.label}>{label}</label>}

      <button
        className={`${styles.trigger} ${isOpen ? styles.open : ''} ${
          disabled ? styles.disabled : ''
        }`}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <span className={styles.selectedText}>
          {selectedOption?.label || placeholder}
        </span>
        <span className={styles.arrow}>▼</span>
      </button>

      {isOpen && !disabled && (
        <div className={styles.menu}>
          {searchable && (
            <input
              ref={searchInputRef}
              type="text"
              placeholder="Buscar..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className={styles.searchInput}
            />
          )}

          <ul className={styles.list} role="listbox">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option) => (
                <li
                  key={option.id}
                  className={`${styles.option} ${
                    option.disabled ? styles.optionDisabled : ''
                  } ${selectedId === option.id ? styles.selected : ''}`}
                  onClick={() => !option.disabled && handleSelect(option.id)}
                  role="option"
                  aria-selected={selectedId === option.id}
                >
                  {option.label}
                </li>
              ))
            ) : (
              <li className={styles.empty}>Nenhuma opção encontrada</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Dropdown;
