// Config local de pruebas: sin dependencias externas; usa el binario vitest
// existente de la ubicacion upstream sin mutarla.
export default {
  test: {
    environment: 'node',
    include: ['*.test.ts'],
  },
};
