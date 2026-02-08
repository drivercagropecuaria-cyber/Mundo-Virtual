import React, { useEffect } from 'react';
import styles from './Modal.module.css';

export type ModalSize = 'small' | 'medium' | 'large';

export interface ModalProps {
  /**
   * Se true, mostra o modal
   */
  isOpen: boolean;

  /**
   * Tamanho do modal
   * @default 'medium'
   */
  size?: ModalSize;

  /**
   * Título do modal
   */
  title?: string;

  /**
   * Conteúdo do modal
   */
  children: React.ReactNode;

  /**
   * Callback ao fechar o modal
   */
  onClose: () => void;

  /**
   * Conteúdo do footer
   */
  footer?: React.ReactNode;

  /**
   * Se true, permite fechar clicando no backdrop
   * @default true
   */
  closeOnBackdropClick?: boolean;

  /**
   * Se true, mostra botão de fechar no header
   * @default true
   */
  showCloseButton?: boolean;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Modal com suporte a 3 tamanhos
 *
 * @example
 * ```tsx
 * <Modal
 *   isOpen={isOpen}
 *   title="Confirmação"
 *   size="small"
 *   onClose={() => setIsOpen(false)}
 *   footer={<button onClick={() => setIsOpen(false)}>Fechar</button>}
 * >
 *   Tem certeza?
 * </Modal>
 * ```
 */
export const Modal: React.FC<ModalProps> = ({
  isOpen,
  size = 'medium',
  title,
  children,
  onClose,
  footer,
  closeOnBackdropClick = true,
  showCloseButton = true,
  className = '',
}) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) {
    return null;
  }

  const handleBackdropClick = () => {
    if (closeOnBackdropClick) {
      onClose();
    }
  };

  return (
    <div className={styles.backdrop} onClick={handleBackdropClick}>
      <div
        className={`${styles.modal} ${styles[size]} ${className}`}
        onClick={(e) => e.stopPropagation()}
      >
        {(title || showCloseButton) && (
          <div className={styles.header}>
            {title && <h2 className={styles.title}>{title}</h2>}
            {showCloseButton && (
              <button
                className={styles.closeButton}
                onClick={onClose}
                aria-label="Fechar modal"
              >
                ✕
              </button>
            )}
          </div>
        )}

        <div className={styles.body}>{children}</div>

        {footer && <div className={styles.footer}>{footer}</div>}
      </div>
    </div>
  );
};

export default Modal;
