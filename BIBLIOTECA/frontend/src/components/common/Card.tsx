import React from 'react';
import styles from './Card.module.css';

export interface CardProps {
  /**
   * Conteúdo do header do card
   */
  header?: React.ReactNode;

  /**
   * Conteúdo principal do card
   */
  children: React.ReactNode;

  /**
   * Conteúdo do footer do card
   */
  footer?: React.ReactNode;

  /**
   * Se true, aplica sombra elevada
   * @default false
   */
  elevated?: boolean;

  /**
   * Classes CSS adicionais
   */
  className?: string;

  /**
   * Classes do header
   */
  headerClassName?: string;

  /**
   * Classes do body
   */
  bodyClassName?: string;

  /**
   * Classes do footer
   */
  footerClassName?: string;
}

/**
 * Componente Card com suporte a header, body e footer
 *
 * @example
 * ```tsx
 * <Card
 *   header={<h2>Título</h2>}
 *   footer={<button>Ação</button>}
 *   elevated
 * >
 *   Conteúdo principal
 * </Card>
 * ```
 */
export const Card: React.FC<CardProps> = ({
  header,
  children,
  footer,
  elevated = false,
  className = '',
  headerClassName = '',
  bodyClassName = '',
  footerClassName = '',
}) => {
  return (
    <div className={`${styles.card} ${elevated ? styles.elevated : ''} ${className}`}>
      {header && (
        <div className={`${styles.header} ${headerClassName}`}>{header}</div>
      )}
      <div className={`${styles.body} ${bodyClassName}`}>{children}</div>
      {footer && (
        <div className={`${styles.footer} ${footerClassName}`}>{footer}</div>
      )}
    </div>
  );
};

export default Card;
