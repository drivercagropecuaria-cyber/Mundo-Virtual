import React, { useState } from 'react';
import styles from './Input.module.css';

export type InputType = 'text' | 'search' | 'email' | 'password' | 'number';

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  /**
   * Tipo de input
   * @default 'text'
   */
  type?: InputType;

  /**
   * Label do input
   */
  label?: string;

  /**
   * Mensagem de erro
   */
  error?: string;

  /**
   * Se true, mostra asterisco (campo obrigatório)
   * @default false
   */
  required?: boolean;

  /**
   * Placeholder do input
   */
  placeholder?: string;

  /**
   * Função de validação customizada
   */
  validate?: (value: string) => string | undefined;

  /**
   * Classes do container
   */
  containerClassName?: string;

  /**
   * Classes do label
   */
  labelClassName?: string;

  /**
   * Classes do wrapper do input
   */
  inputWrapperClassName?: string;
}

/**
 * Componente Input com suporte a validação
 *
 * @example
 * ```tsx
 * <Input
 *   label="Email"
 *   type="email"
 *   placeholder="seu@email.com"
 *   required
 *   validate={(value) => !value.includes('@') ? 'Email inválido' : undefined}
 * />
 * <Input type="search" placeholder="Pesquisar..." />
 * ```
 */
export const Input: React.FC<InputProps> = ({
  type = 'text',
  label,
  error: externalError,
  required = false,
  placeholder,
  validate,
  containerClassName = '',
  labelClassName = '',
  inputWrapperClassName = '',
  onChange,
  value,
  ...props
}) => {
  const [internalError, setInternalError] = useState<string | undefined>();
  const [isFocused, setIsFocused] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.currentTarget.value;

    if (validate && newValue) {
      const validationError = validate(newValue);
      setInternalError(validationError);
    } else {
      setInternalError(undefined);
    }

    onChange?.(e);
  };

  const displayError = externalError || internalError;
  const hasError = !!displayError;

  return (
    <div className={`${styles.container} ${containerClassName}`}>
      {label && (
        <label className={`${styles.label} ${labelClassName}`}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      <div
        className={`${styles.inputWrapper} ${inputWrapperClassName} ${
          isFocused ? styles.focused : ''
        } ${hasError ? styles.error : ''}`}
      >
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className={styles.input}
          {...props}
        />
      </div>
      {displayError && <span className={styles.errorMessage}>{displayError}</span>}
    </div>
  );
};

export default Input;
