import Pagination from './Pagination';

export default {
  title: 'Shared/Pagination',
  component: Pagination,
};

export const Default = () => (
  <Pagination page={2} totalPages={5} onPageChange={() => {}} />
);
