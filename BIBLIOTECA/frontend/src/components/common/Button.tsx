import React from 'react';
import styles from './Button.module.css';

export type ButtonVariant = 'primary' | 'secondary' | 'danger';
export type ButtonSize = 'small' | 'medium' | 'large';

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Variante visual do botão
   * @default 'primary'
   */
  variant?: ButtonVariant;

  /**
   * Tamanho do botão
   * @default 'medium'
   */
  size?: ButtonSize;

  /**
   * Se true, o botão fica desabilitado
   * @default false
   */
  disabled?: boolean;

  /**
   * Se true, mostra estado de carregamento
   * @default false
   */
  loading?: boolean;

  /**
   * Conteúdo do botão
   */
  children: React.ReactNode;

  /**
   * Callback executado ao clicar
   */
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
}

/**
 * Componente Button reutilizável
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="large">Clique aqui</Button>
 * <Button variant="danger" disabled>Deletar</Button>
 * <Button loading>Salvando...</Button>
 * ```
 */
export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  children,
  className,
  ...props
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]} ${
        disabled || loading ? styles.disabled : ''
      } ${className || ''}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className={styles.spinner} />}
      {children}
    </button>
  );
};

export default Button;
