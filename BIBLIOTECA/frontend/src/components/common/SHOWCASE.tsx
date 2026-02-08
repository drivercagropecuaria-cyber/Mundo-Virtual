/**
 * SHOWCASE DE COMPONENTES
 * Demonstra o uso de todos os componentes da biblioteca
 * 
 * Este arquivo é um exemplo de como usar a biblioteca de componentes.
 * Remove-o ou adapte conforme necessário.
 */

import React, { useState } from 'react';
import { Button } from './Button';
import { Badge } from './Badge';
import { Card } from './Card';
import { Input } from './Input';
import { Spinner } from './Spinner';
import { Modal } from './Modal';
import { Dropdown, type DropdownOption } from './Dropdown';
import { Pagination } from './Pagination';
import { Tabs, type TabItem } from './Tabs';
import { Breadcrumbs } from './Breadcrumbs';
import { Avatar } from './Avatar';
import { Alert } from './Alert';

/**
 * Componente de demonstração de todos os componentes
 * Mostra casos de uso típicos para cada um
 */
export const ComponentShowcase: React.FC = () => {
  // Estados para componentes interativos
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedDropdown, setSelectedDropdown] = useState<string | number>('opt1');
  const [currentPage, setCurrentPage] = useState(1);
  const [activeTab, setActiveTab] = useState('tab1');
  const [inputValue, setInputValue] = useState('');

  // Opções para o dropdown
  const dropdownOptions: DropdownOption[] = [
    { id: 'opt1', label: 'Opção 1' },
    { id: 'opt2', label: 'Opção 2' },
    { id: 'opt3', label: 'Opção 3', disabled: true },
    { id: 'opt4', label: 'Opção 4' },
  ];

  // Abas
  const tabs: TabItem[] = [
    {
      id: 'tab1',
      label: 'Visão Geral',
      content: <p>Conteúdo da primeira aba</p>,
    },
    {
      id: 'tab2',
      label: 'Detalhes',
      content: <p>Conteúdo da segunda aba com mais informações</p>,
    },
    {
      id: 'tab3',
      label: 'Configurações',
      content: <p>Configurações adicionais aqui</p>,
    },
  ];

  return (
    <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>📚 Showcase - Component Library</h1>

      {/* Seção de Navegação */}
      <section style={{ marginBottom: '40px' }}>
        <h2>🧭 Navegação - Breadcrumbs</h2>
        <Breadcrumbs
          items={[
            { label: 'Home', href: '#' },
            { label: 'Componentes', href: '#' },
            { label: 'Showcase' },
          ]}
        />
      </section>

      {/* Seção de Alertas */}
      <section style={{ marginBottom: '40px' }}>
        <h2>⚠️ Alertas</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <Alert
            variant="success"
            title="Sucesso"
            message="Operação realizada com sucesso!"
            closeable
          />
          <Alert
            variant="warning"
            title="Aviso"
            message="Atenção: verifique os dados antes de prosseguir"
            closeable
          />
          <Alert
            variant="danger"
            title="Erro"
            message="Ocorreu um erro na operação"
            closeable
          />
          <Alert
            variant="info"
            title="Informação"
            message="Esta é uma mensagem informativa"
            closeable
          />
        </div>
      </section>

      {/* Seção de Botões */}
      <section style={{ marginBottom: '40px' }}>
        <h2>🔘 Botões</h2>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <Button variant="primary">Primary</Button>
          <Button variant="primary" size="small">Small</Button>
          <Button variant="primary" size="large">Large</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="danger">Danger</Button>
          <Button disabled>Disabled</Button>
          <Button loading>Loading...</Button>
        </div>
      </section>

      {/* Seção de Badges */}
      <section style={{ marginBottom: '40px' }}>
        <h2>🏷️ Badges</h2>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <Badge variant="success">Success</Badge>
          <Badge variant="warning">Warning</Badge>
          <Badge variant="danger">Danger</Badge>
          <Badge variant="info">Info</Badge>
        </div>
      </section>

      {/* Seção de Avatars */}
      <section style={{ marginBottom: '40px' }}>
        <h2>👤 Avatars</h2>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Avatar name="João Silva" size="small" backgroundColor="#0066cc" />
          <Avatar name="Maria Santos" size="medium" backgroundColor="#ff6b6b" withBorder />
          <Avatar name="Pedro Costa" size="large" backgroundColor="#4caf50" />
          <Avatar src="https://via.placeholder.com/64" name="Imagem" size="large" />
        </div>
      </section>

      {/* Seção de Inputs */}
      <section style={{ marginBottom: '40px' }}>
        <h2>📝 Inputs</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '400px' }}>
          <Input
            label="Nome"
            type="text"
            placeholder="Digite seu nome"
            required
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <Input
            label="Email"
            type="email"
            placeholder="seu@email.com"
            validate={(value) => {
              if (!value.includes('@')) return 'Email inválido';
            }}
          />
          <Input label="Busca" type="search" placeholder="Pesquisar..." />
        </div>
      </section>

      {/* Seção de Spinner */}
      <section style={{ marginBottom: '40px' }}>
        <h2>⏳ Loading Spinner</h2>
        <div style={{ display: 'flex', gap: '40px' }}>
          <div style={{ textAlign: 'center' }}>
            <Spinner size="small" />
            <p>Small</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <Spinner size="medium" message="Carregando..." />
            <p>Medium</p>
          </div>
          <div style={{ textAlign: 'center' }}>
            <Spinner size="large" />
            <p>Large</p>
          </div>
        </div>
      </section>

      {/* Seção de Card */}
      <section style={{ marginBottom: '40px' }}>
        <h2>📦 Card</h2>
        <Card
          header={<h3>Título do Card</h3>}
          elevated
          footer={
            <div style={{ display: 'flex', gap: '8px' }}>
              <Button variant="secondary" size="small">
                Cancelar
              </Button>
              <Button variant="primary" size="small">
                Salvar
              </Button>
            </div>
          }
        >
          <p>
            Este é um exemplo de card com header, body e footer. Você pode adicionar qualquer
            conteúdo aqui.
          </p>
          <p>
            O card possui uma série de props para customização como header, footer, elevated, etc.
          </p>
        </Card>
      </section>

      {/* Seção de Dropdown */}
      <section style={{ marginBottom: '40px' }}>
        <h2>📋 Dropdown</h2>
        <div style={{ maxWidth: '300px' }}>
          <Dropdown
            label="Selecione uma opção"
            options={dropdownOptions}
            selectedId={selectedDropdown}
            onChange={setSelectedDropdown}
            searchable
          />
        </div>
        <p>Selecionado: {selectedDropdown}</p>
      </section>

      {/* Seção de Pagination */}
      <section style={{ marginBottom: '40px' }}>
        <h2>📑 Pagination</h2>
        <Pagination
          currentPage={currentPage}
          totalPages={10}
          onPageChange={setCurrentPage}
          maxPagesToShow={5}
        />
        <p>Página atual: {currentPage}</p>
      </section>

      {/* Seção de Tabs */}
      <section style={{ marginBottom: '40px' }}>
        <h2>🗂️ Tabs</h2>
        <Tabs tabs={tabs} activeTabId={activeTab} onTabChange={setActiveTab} />
      </section>

      {/* Seção de Modal */}
      <section style={{ marginBottom: '40px' }}>
        <h2>🪟 Modal</h2>
        <Button onClick={() => setIsModalOpen(true)}>Abrir Modal</Button>
        <Modal
          isOpen={isModalOpen}
          title="Modal Example"
          onClose={() => setIsModalOpen(false)}
          footer={
            <Button variant="primary" onClick={() => setIsModalOpen(false)}>
              Fechar
            </Button>
          }
        >
          <p>Este é um exemplo de modal. Clique no botão para fechar ou clique fora do modal.</p>
        </Modal>
      </section>
    </div>
  );
};

export default ComponentShowcase;
