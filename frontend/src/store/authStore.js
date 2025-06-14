import { create } from 'zustand';
import { authService } from '../services/auth';

const useAuthStore = create((set) => ({
  user: null,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      await authService.login(email, password);
      const user = await authService.getCurrentUser();
      set({ user, isLoading: false });
      return true;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Login failed', isLoading: false });
      return false;
    }
  },

  register: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      await authService.register(email, password);
      return true;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Registration failed', isLoading: false });
      return false;
    }
  },

  logout: () => {
    authService.logout();
    set({ user: null });
  },

  checkAuth: async () => {
    if (!authService.isAuthenticated()) {
      return;
    }
    try {
      const user = await authService.getCurrentUser();
      set({ user });
    } catch (error) {
      authService.logout();
    }
  }
}));

export default useAuthStore;
