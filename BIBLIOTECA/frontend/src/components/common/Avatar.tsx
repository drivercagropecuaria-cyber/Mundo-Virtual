import React from 'react';
import styles from './Avatar.module.css';

export type AvatarSize = 'small' | 'medium' | 'large';

export interface AvatarProps {
  /**
   * URL da imagem
   */
  src?: string;

  /**
   * Nome/iniciais para fallback
   */
  name?: string;

  /**
   * Tamanho do avatar
   * @default 'medium'
   */
  size?: AvatarSize;

  /**
   * Cor de background para fallback (hex ou CSS)
   */
  backgroundColor?: string;

  /**
   * Se true, exibe borda ao redor
   */
  withBorder?: boolean;

  /**
   * Classes CSS adicionais
   */
  className?: string;

  /**
   * Alt text para imagem
   */
  alt?: string;
}

/**
 * Componente Avatar para exibir imagens de perfil ou iniciais
 *
 * @example
 * ```tsx
 * <Avatar src="https://example.com/avatar.jpg" name="João Silva" size="large" />
 * <Avatar name="AB" size="medium" backgroundColor="#0066cc" withBorder />
 * ```
 */
export const Avatar: React.FC<AvatarProps> = ({
  src,
  name = '?',
  size = 'medium',
  backgroundColor,
  withBorder = false,
  className = '',
  alt,
}) => {
  const initials = name
    ?.split(' ')
    .slice(0, 2)
    .map((word) => word.charAt(0))
    .join('')
    .toUpperCase() || '?';

  return (
    <div
      className={`${styles.avatar} ${styles[size]} ${
        withBorder ? styles.bordered : ''
      } ${className}`}
      style={!src ? { backgroundColor: backgroundColor || '#e0e0e0' } : undefined}
      title={name}
    >
      {src ? (
        <img src={src} alt={alt || name} className={styles.image} />
      ) : (
        <span className={styles.initials}>{initials}</span>
      )}
    </div>
  );
};

export default Avatar;
