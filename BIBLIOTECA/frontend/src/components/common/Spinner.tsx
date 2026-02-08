import React from 'react';
import styles from './Spinner.module.css';

export type SpinnerSize = 'small' | 'medium' | 'large';

export interface SpinnerProps {
  /**
   * Tamanho do spinner
   * @default 'medium'
   */
  size?: SpinnerSize;

  /**
   * Mensagem opcional
   */
  message?: string;

  /**
   * Cor customizada (valor hex ou CSS)
   */
  color?: string;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente de loading spinner
 *
 * @example
 * ```tsx
 * <Spinner size="small" />
 * <Spinner size="large" message="Carregando..." />
 * ```
 */
export const Spinner: React.FC<SpinnerProps> = ({
  size = 'medium',
  message,
  color = '#0066cc',
  className = '',
}) => {
  return (
    <div className={`${styles.container} ${className}`}>
      <div
        className={`${styles.spinner} ${styles[size]}`}
        style={color ? { borderTopColor: color } : undefined}
      />
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
};

export default Spinner;
