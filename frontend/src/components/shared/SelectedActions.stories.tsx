import React, { useState } from 'react';
import SelectedActions from './SelectedActions';

export default {
  title: 'Shared/SelectedActions',
  component: SelectedActions,
};

export const Default = () => {
  const [count, setCount] = useState(2);
  const [sending, setSending] = useState(false);

  return (
    <div className="bg-white dark:bg-gray-900 p-6 max-w-md mx-auto">
      <SelectedActions
        selectedCount={count}
        isSending={sending}
        variant="primary"
        onSend={() => {
          setSending(true);
          setTimeout(() => {
            alert('Email sent!');
            setSending(false);
          }, 1000);
        }}
        onClear={() => setCount(0)}
      />
    </div>
  );
};

export const NoneSelected = () => (
  <SelectedActions
    selectedCount={0}
    onSend={() => {}}
    onClear={() => {}}
    variant="primary"
  />
);

export const SendingState = () => (
  <SelectedActions
    selectedCount={3}
    onSend={() => {}}
    onClear={() => {}}
    isSending={true}
    variant="primary"
  />
);


