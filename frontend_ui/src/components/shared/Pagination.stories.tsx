import React, { useState } from 'react';
import Pagination from './Pagination';

export default {
  title: 'Shared/Pagination',
  component: Pagination,
};

export const Default = () => {
  const [page, setPage] = useState(1);
  return (
    <Pagination
      page={page}
      totalPages={5}
      onPageChange={setPage}
      variant="default"
    />
  );
};

export const PrimaryVariant = () => {
  const [page, setPage] = useState(2);
  return (
    <Pagination
      page={page}
      totalPages={8}
      onPageChange={setPage}
      variant="primary"
    />
  );
};

export const LastPageDisabled = () => {
  return (
    <Pagination
      page={10}
      totalPages={10}
      onPageChange={() => {}}
      variant="danger"
    />
  );
};
