import '@testing-library/jest-dom';
import { vi } from 'vitest';

vi.mock('axios', async (importActual) => {
  const actual = await importActual();
  const mockAxios = {
    ...actual,
    default: {
      ...actual.default,
      create: () => ({
        get: vi.fn().mockResolvedValue([]),
        post: vi.fn().mockResolvedValue({}),
        put: vi.fn().mockResolvedValue({}),
        delete: vi.fn().mockResolvedValue({}),
        request: vi.fn().mockResolvedValue({ data: {} }),
        interceptors: {
          request: { use: vi.fn(), eject: vi.fn(), clear: vi.fn() },
          response: { use: vi.fn(), eject: vi.fn(), clear: vi.fn() },
        },
      }),
    },
  };
  return mockAxios;
});

const store = {};
const localStorageMock = {
  getItem: vi.fn((key) => store[key] ?? null),
  setItem: vi.fn((key, value) => { store[key] = String(value); }),
  removeItem: vi.fn((key) => { delete store[key]; }),
  clear: vi.fn(() => { Object.keys(store).forEach(k => delete store[k]); }),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock, writable: true });

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false, media: query, onchange: null,
    addListener: vi.fn(), removeListener: vi.fn(),
    addEventListener: vi.fn(), removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

window.scrollTo = vi.fn();
