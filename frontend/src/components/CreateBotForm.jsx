import { useState } from 'react';
import useBotStore from '../store/botStore';

export default function CreateBotForm({ onClose }) {
  const [formData, setFormData] = useState({
    bot_name: '',
    bot_token: ''
  });
  const { createBot } = useBotStore();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Отправляем только те поля, которые ожидает API
      const botData = {
        bot_token: formData.bot_token,
        bot_name: formData.bot_name || null
      };
      
      await createBot(botData);
      onClose();
    } catch (error) {
      console.error('Ошибка создания бота:', error.response?.data || error);
      alert(`Ошибка: ${error.response?.data?.detail || 'Не удалось создать бота'}`);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">Создать нового бота</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Название бота (необязательно)
            </label>
            <input
              type="text"
              value={formData.bot_name}
              onChange={(e) => setFormData({ ...formData, bot_name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Мой бот"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Telegram токен *
            </label>
            <input
              type="text"
              required
              value={formData.bot_token}
              onChange={(e) => setFormData({ ...formData, bot_token: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="123456:ABC-DEF..."
            />
            <p className="mt-1 text-sm text-gray-500">
              Получите токен у @BotFather в Telegram
            </p>
          </div>
          
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
            >
              Отмена
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
