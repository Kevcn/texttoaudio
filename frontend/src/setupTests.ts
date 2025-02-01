import '@testing-library/jest-dom';

// Mock URL.createObjectURL and URL.revokeObjectURL
global.URL.createObjectURL = jest.fn();
global.URL.revokeObjectURL = jest.fn();

// Mock window.HTMLMediaElement
window.HTMLMediaElement.prototype.load = jest.fn();
window.HTMLMediaElement.prototype.play = jest.fn();
window.HTMLMediaElement.prototype.pause = jest.fn();

// Reset all mocks after each test
afterEach(() => {
  jest.clearAllMocks();
}); 