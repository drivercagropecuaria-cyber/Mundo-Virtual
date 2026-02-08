import React from 'react';
import styles from './Pagination.module.css';

export interface PaginationProps {
  /**
   * Página atual (1-indexed)
   */
  currentPage: number;

  /**
   * Total de páginas
   */
  totalPages: number;

  /**
   * Callback ao mudar de página
   */
  onPageChange: (page: number) => void;

  /**
   * Se true, desabilita os botões
   */
  disabled?: boolean;

  /**
   * Máximo de números de página a exibir
   * @default 5
   */
  maxPagesToShow?: number;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Pagination para navegação entre páginas
 *
 * @example
 * ```tsx
 * <Pagination
 *   currentPage={1}
 *   totalPages={10}
 *   onPageChange={(page) => console.log(page)}
 * />
 * ```
 */
export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  disabled = false,
  maxPagesToShow = 5,
  className = '',
}) => {
  const startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
  const endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
  const adjustedStartPage = Math.max(1, endPage - maxPagesToShow + 1);

  const pages = Array.from(
    { length: adjustedStartPage > startPage ? endPage - adjustedStartPage + 1 : maxPagesToShow },
    (_, i) => adjustedStartPage + i
  );

  const handlePageChange = (page: number) => {
    if (!disabled && page >= 1 && page <= totalPages && page !== currentPage) {
      onPageChange(page);
    }
  };

  return (
    <nav className={`${styles.pagination} ${className}`} aria-label="Paginação">
      <button
        className={styles.button}
        onClick={() => handlePageChange(currentPage - 1)}
        disabled={disabled || currentPage === 1}
        aria-label="Página anterior"
      >
        ← Anterior
      </button>

      <div className={styles.pages}>
        {adjustedStartPage > 1 && (
          <>
            <button
              className={`${styles.pageButton} ${styles.number}`}
              onClick={() => handlePageChange(1)}
              disabled={disabled}
            >
              1
            </button>
            {adjustedStartPage > 2 && <span className={styles.ellipsis}>…</span>}
          </>
        )}

        {pages.map((page) => (
          <button
            key={page}
            className={`${styles.pageButton} ${styles.number} ${
              page === currentPage ? styles.active : ''
            }`}
            onClick={() => handlePageChange(page)}
            disabled={disabled}
            aria-current={page === currentPage ? 'page' : undefined}
          >
            {page}
          </button>
        ))}

        {endPage < totalPages && (
          <>
            {endPage < totalPages - 1 && <span className={styles.ellipsis}>…</span>}
            <button
              className={`${styles.pageButton} ${styles.number}`}
              onClick={() => handlePageChange(totalPages)}
              disabled={disabled}
            >
              {totalPages}
            </button>
          </>
        )}
      </div>

      <button
        className={styles.button}
        onClick={() => handlePageChange(currentPage + 1)}
        disabled={disabled || currentPage === totalPages}
        aria-label="Próxima página"
      >
        Próxima →
      </button>
    </nav>
  );
};

export default Pagination;
