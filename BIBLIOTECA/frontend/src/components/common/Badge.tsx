import React from 'react';
import styles from './Badge.module.css';

export type BadgeVariant = 'success' | 'warning' | 'danger' | 'info';

export interface BadgeProps {
  /**
   * Variante de cor do badge
   * @default 'info'
   */
  variant?: BadgeVariant;

  /**
   * Conteúdo do badge
   */
  children: React.ReactNode;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Badge para destacar status ou categorias
 *
 * @example
 * ```tsx
 * <Badge variant="success">Ativo</Badge>
 * <Badge variant="danger">Erro</Badge>
 * <Badge variant="warning">Aviso</Badge>
 * <Badge variant="info">Informação</Badge>
 * ```
 */
export const Badge: React.FC<BadgeProps> = ({
  variant = 'info',
  children,
  className = '',
}) => {
  return (
    <span className={`${styles.badge} ${styles[variant]} ${className}`}>
      {children}
    </span>
  );
};

export default Badge;
