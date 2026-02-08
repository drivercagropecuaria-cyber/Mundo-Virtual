import React, { useState, useEffect } from 'react';
import styles from './Alert.module.css';

export type AlertVariant = 'success' | 'warning' | 'danger' | 'info';

export interface AlertProps {
  /**
   * Variante de tipo do alerta
   * @default 'info'
   */
  variant?: AlertVariant;

  /**
   * Título do alerta
   */
  title?: string;

  /**
   * Mensagem do alerta
   */
  message: string;

  /**
   * Se true, exibe botão de fechar
   * @default true
   */
  closeable?: boolean;

  /**
   * Tempo (em ms) para auto-fechar (0 = nunca)
   * @default 0
   */
  autoCloseDuration?: number;

  /**
   * Callback ao fechar
   */
  onClose?: () => void;

  /**
   * Classes CSS adicionais
   */
  className?: string;
}

/**
 * Componente Alert/Toast para mostrar mensagens
 *
 * @example
 * ```tsx
 * <Alert
 *   variant="success"
 *   title="Sucesso"
 *   message="Operação concluída com sucesso"
 *   closeable
 *   autoCloseDuration={3000}
 * />
 * ```
 */
export const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  message,
  closeable = true,
  autoCloseDuration = 0,
  onClose,
  className = '',
}) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (autoCloseDuration > 0) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        onClose?.();
      }, autoCloseDuration);

      return () => clearTimeout(timer);
    }
  }, [autoCloseDuration, onClose]);

  if (!isVisible) {
    return null;
  }

  const handleClose = () => {
    setIsVisible(false);
    onClose?.();
  };

  const iconMap: Record<AlertVariant, string> = {
    success: '✓',
    warning: '⚠',
    danger: '✕',
    info: 'ℹ',
  };

  return (
    <div className={`${styles.alert} ${styles[variant]} ${className}`} role="alert">
      <div className={styles.icon}>{iconMap[variant]}</div>
      <div className={styles.content}>
        {title && <h4 className={styles.title}>{title}</h4>}
        <p className={styles.message}>{message}</p>
      </div>
      {closeable && (
        <button
          className={styles.closeButton}
          onClick={handleClose}
          aria-label="Fechar alerta"
        >
          ✕
        </button>
      )}
    </div>
  );
};

export default Alert;
