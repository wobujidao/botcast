import { useEffect, useState } from 'react';
import useBotStore from '../store/botStore';

export default function BotList() {
  const { bots, fetchBots, deleteBot, startBot, stopBot, isLoading } = useBotStore();
  const [selectedBot, setSelectedBot] = useState(null);

  useEffect(() => {
    fetchBots();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Вы уверены, что хотите удалить этого бота?')) {
      await deleteBot(id);
    }
  };

  const handleToggleBot = async (bot) => {
    try {
      if (bot.is_running) {
        await stopBot(bot.id);
      } else {
        await startBot(bot.id);
      }
      await fetchBots(); // Обновляем список
    } catch (error) {
      console.error('Ошибка переключения статуса бота:', error);
    }
  };

  if (isLoading && bots.length === 0) {
    return <div className="text-center py-4">Загрузка...</div>;
  }

  if (bots.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        У вас пока нет ботов. Создайте первого!
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {bots.map((bot) => (
        <div
          key={bot.id}
          className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
        >
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900">{bot.name}</h3>
            <p className="mt-1 text-sm text-gray-500">{bot.description}</p>
            
            <div className="mt-4">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                bot.is_running 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {bot.is_running ? 'Запущен' : 'Остановлен'}
              </span>
            </div>

            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => handleToggleBot(bot)}
                className={`inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded ${
                  bot.is_running
                    ? 'bg-red-600 text-white hover:bg-red-700'
                    : 'bg-green-600 text-white hover:bg-green-700'
                }`}
              >
                {bot.is_running ? 'Остановить' : 'Запустить'}
              </button>
              
              <button
                onClick={() => setSelectedBot(bot)}
                className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
              >
                Настройки
              </button>
              
              <button
                onClick={() => handleDelete(bot.id)}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
