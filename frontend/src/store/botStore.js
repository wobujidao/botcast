import { create } from 'zustand';
import { botService } from '../services/bots';

const useBotStore = create((set, get) => ({
  bots: [],
  selectedBot: null,
  isLoading: false,
  error: null,

  fetchBots: async () => {
    set({ isLoading: true, error: null });
    try {
      const bots = await botService.getAll();
      set({ bots, isLoading: false });
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Ошибка загрузки ботов', isLoading: false });
    }
  },

  createBot: async (botData) => {
    set({ isLoading: true, error: null });
    try {
      const newBot = await botService.create(botData);
      set((state) => ({ 
        bots: [...state.bots, newBot], 
        isLoading: false 
      }));
      return newBot;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Ошибка создания бота', isLoading: false });
      throw error;
    }
  },

  updateBot: async (id, botData) => {
    set({ isLoading: true, error: null });
    try {
      const updatedBot = await botService.update(id, botData);
      set((state) => ({ 
        bots: state.bots.map(bot => bot.id === id ? updatedBot : bot),
        selectedBot: state.selectedBot?.id === id ? updatedBot : state.selectedBot,
        isLoading: false 
      }));
      return updatedBot;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Ошибка обновления бота', isLoading: false });
      throw error;
    }
  },

  deleteBot: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await botService.delete(id);
      set((state) => ({ 
        bots: state.bots.filter(bot => bot.id !== id),
        selectedBot: state.selectedBot?.id === id ? null : state.selectedBot,
        isLoading: false 
      }));
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Ошибка удаления бота', isLoading: false });
      throw error;
    }
  },

  selectBot: (bot) => {
    set({ selectedBot: bot });
  },

  startBot: async (id) => {
    try {
      const result = await botService.start(id);
      // Обновляем статус бота в списке
      const status = await botService.getStatus(id);
      set((state) => ({ 
        bots: state.bots.map(bot => 
          bot.id === id ? { ...bot, is_running: status.is_running } : bot
        )
      }));
      return result;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Ошибка запуска бота' });
      throw error;
    }
  },

  stopBot: async (id) => {
    try {
      const result = await botService.stop(id);
      // Обновляем статус бота в списке
      set((state) => ({ 
        bots: state.bots.map(bot => 
          bot.id === id ? { ...bot, is_running: false } : bot
        )
      }));
      return result;
    } catch (error) {
      set({ error: error.response?.data?.detail || 'Ошибка остановки бота' });
      throw error;
    }
  }
}));

export default useBotStore;
