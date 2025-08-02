function ErrorBanner({ message }) {
  return (
    <div className="p-4 mb-4 bg-red-100 text-red-800 rounded">
      Error: {message}
    </div>
  );
}

export default ErrorBanner;
