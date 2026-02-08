import React from 'react';
import styles from './Breadcrumbs.module.css';

export interface BreadcrumbItem {
  /**
   * Rótulo do breadcrumb
   */
  label: string;

  /**
   * URL ou href (opcional)
   */
  href?: string;

  /**
   * Callback ao clicar
   */
  onClick?: () => void;
}

export interface BreadcrumbsProps {
  /**
   * Array de itens de breadcrumb
   */
  items: BreadcrumbItem[];

  /**
   * Separador entre itens
   * @default '/'
   */
  separator?: string;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Breadcrumbs para navegação hierárquica
 *
 * @example
 * ```tsx
 * <Breadcrumbs
 *   items={[
 *     { label: 'Home', href: '/' },
 *     { label: 'Biblioteca', href: '/biblioteca' },
 *     { label: 'Detalhes' }
 *   ]}
 * />
 * ```
 */
export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  separator = '/',
  className = '',
}) => {
  return (
    <nav className={`${styles.breadcrumbs} ${className}`} aria-label="Breadcrumbs">
      <ol className={styles.list}>
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          const isClickable = !!item.href || !!item.onClick;

          return (
            <li key={index} className={styles.item}>
              {isClickable ? (
                <a
                  href={item.href}
                  onClick={(e) => {
                    if (item.onClick) {
                      e.preventDefault();
                      item.onClick();
                    }
                  }}
                  className={`${styles.link} ${isLast ? styles.current : ''}`}
                  aria-current={isLast ? 'page' : undefined}
                >
                  {item.label}
                </a>
              ) : (
                <span className={`${styles.text} ${isLast ? styles.current : ''}`}>
                  {item.label}
                </span>
              )}

              {!isLast && <span className={styles.separator}>{separator}</span>}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

export default Breadcrumbs;
