import React, { useState, useEffect } from 'react';
import {
  Plus,
  Trophy,
  Users,
  Target,
  TrendingUp,
  Crown,
  Medal,
  Star,
  Calendar,
  BarChart3,
  UserPlus,
  Edit3,
  Save,
  X
} from 'lucide-react';

// Типы данных
interface Player {
  id: string;
  name: string;
  totalGames: number;
  wins: number;
  losses: number;
  winRate: number;
  totalScore: number;
  bestRole: string;
  lastPlayed: string;
  avatar?: string;
}

interface Game {
  id: string;
  date: string;
  players: string[];
  winner: 'mafia' | 'civilians' | 'neutral';
  duration: number;
  mvp?: string;
}

const MafiaStatsApp = () => {
  const [players, setPlayers] = useState<Player[]>([
    {
      id: '1',
      name: 'Алексей Волков',
      totalGames: 45,
      wins: 28,
      losses: 17,
      winRate: 62.2,
      totalScore: 2840,
      bestRole: 'Комиссар',
      lastPlayed: '2024-12-15',
      avatar: '🕵️'
    },
    {
      id: '2',
      name: 'Мария Петрова',
      totalGames: 38,
      wins: 25,
      losses: 13,
      winRate: 65.8,
      totalScore: 2650,
      bestRole: 'Мафия',
      lastPlayed: '2024-12-14',
      avatar: '👑'
    },
    {
      id: '3',
      name: 'Дмитрий Козлов',
      totalGames: 52,
      wins: 30,
      losses: 22,
      winRate: 57.7,
      totalScore: 2920,
      bestRole: 'Доктор',
      lastPlayed: '2024-12-13',
      avatar: '🏥'
    },
    {
      id: '4',
      name: 'Анна Сидорова',
      totalGames: 29,
      wins: 18,
      losses: 11,
      winRate: 62.1,
      totalScore: 1890,
      bestRole: 'Мирный',
      lastPlayed: '2024-12-12',
      avatar: '🌟'
    },
    {
      id: '5',
      name: 'Игорь Морозов',
      totalGames: 41,
      wins: 22,
      losses: 19,
      winRate: 53.7,
      totalScore: 2110,
      bestRole: 'Мафия',
      lastPlayed: '2024-12-11',
      avatar: '🎭'
    }
  ]);

  const [games, setGames] = useState<Game[]>([
    {
      id: '1',
      date: '2024-12-15',
      players: ['Алексей Волков', 'Мария Петрова', 'Дмитрий Козлов'],
      winner: 'civilians',
      duration: 45,
      mvp: 'Алексей Волков'
    },
    {
      id: '2',
      date: '2024-12-14',
      players: ['Мария Петрова', 'Анна Сидорова', 'Игорь Морозов'],
      winner: 'mafia',
      duration: 38,
      mvp: 'Мария Петрова'
    }
  ]);

  const [activeTab, setActiveTab] = useState<'leaderboard' | 'games' | 'add-game'>('leaderboard');
  const [showAddPlayer, setShowAddPlayer] = useState(false);
  const [newPlayerName, setNewPlayerName] = useState('');
  const [editingPlayer, setEditingPlayer] = useState<string | null>(null);

  const sortedPlayers = [...players].sort((a, b) => b.totalScore - a.totalScore);
  const totalGames = games.length;
  const totalPlayers = players.length;

  const handleAddPlayer = () => {
    if (newPlayerName.trim()) {
      const newPlayer: Player = {
        id: Date.now().toString(),
        name: newPlayerName.trim(),
        totalGames: 0,
        wins: 0,
        losses: 0,
        winRate: 0,
        totalScore: 0,
        bestRole: '-',
        lastPlayed: '-',
        avatar: '👤'
      };
      setPlayers([...players, newPlayer]);
      setNewPlayerName('');
      setShowAddPlayer(false);
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'Мафия': return 'text-red-500 bg-red-100';
      case 'Комиссар': return 'text-blue-500 bg-blue-100';
      case 'Доктор': return 'text-green-500 bg-green-100';
      case 'Мирный': return 'text-gray-500 bg-gray-100';
      default: return 'text-gray-500 bg-gray-100';
    }
  };

  const getWinnerColor = (winner: string) => {
    switch (winner) {
      case 'mafia': return 'text-red-500 bg-red-100';
      case 'civilians': return 'text-blue-500 bg-blue-100';
      case 'neutral': return 'text-yellow-500 bg-yellow-100';
      default: return 'text-gray-500 bg-gray-100';
    }
  };

  const getWinnerText = (winner: string) => {
    switch (winner) {
      case 'mafia': return 'Мафия';
      case 'civilians': return 'Мирные';
      case 'neutral': return 'Ничья';
      default: return 'Неизвестно';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-red-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Trophy className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Мафия Клуб</h1>
                <p className="text-gray-600">Статистика студенческого клуба</p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <Users className="w-4 h-4" />
                  <span>{totalPlayers} игроков</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Calendar className="w-4 h-4" />
                  <span>{totalGames} игр</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('leaderboard')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'leaderboard'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Trophy className="w-4 h-4" />
                <span>Таблица лидеров</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('games')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'games'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center space-x-2">
                <BarChart3 className="w-4 h-4" />
                <span>История игр</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('add-game')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'add-game'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Plus className="w-4 h-4" />
                <span>Добавить игру</span>
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'leaderboard' && (
          <div className="space-y-6">
            {/* Top Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Всего игр</p>
                    <p className="text-2xl font-bold text-gray-900">{totalGames}</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                    <Target className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Активных игроков</p>
                    <p className="text-2xl font-bold text-gray-900">{totalPlayers}</p>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                    <Users className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Средний винрейт</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {(players.reduce((acc, p) => acc + p.winRate, 0) / players.length).toFixed(1)}%
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </div>
            </div>

            {/* Add Player Button */}
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">Таблица лидеров</h2>
              <button
                onClick={() => setShowAddPlayer(!showAddPlayer)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <UserPlus className="w-4 h-4" />
                <span>Добавить игрока</span>
              </button>
            </div>

            {/* Add Player Form */}
            {showAddPlayer && (
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
                <div className="flex items-center space-x-4">
                  <input
                    type="text"
                    value={newPlayerName}
                    onChange={(e) => setNewPlayerName(e.target.value)}
                    placeholder="Имя игрока"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onKeyPress={(e) => e.key === 'Enter' && handleAddPlayer()}
                  />
                  <button
                    onClick={handleAddPlayer}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
                  >
                    <Save className="w-4 h-4" />
                    <span>Добавить</span>
                  </button>
                  <button
                    onClick={() => setShowAddPlayer(false)}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors flex items-center space-x-2"
                  >
                    <X className="w-4 h-4" />
                    <span>Отмена</span>
                  </button>
                </div>
              </div>
            )}

            {/* Leaderboard Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Место
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Игрок
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Очки
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Игры
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Винрейт
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Лучшая роль
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Последняя игра
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {sortedPlayers.map((player, index) => (
                      <tr key={player.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            {index === 0 && <Crown className="w-5 h-5 text-yellow-500 mr-2" />}
                            {index === 1 && <Medal className="w-5 h-5 text-gray-400 mr-2" />}
                            {index === 2 && <Medal className="w-5 h-5 text-amber-600 mr-2" />}
                            <span className="text-sm font-medium text-gray-900">#{index + 1}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <span className="text-2xl mr-3">{player.avatar}</span>
                            <span className="text-sm font-medium text-gray-900">{player.name}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="text-sm font-bold text-blue-600">{player.totalScore}</span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {player.totalGames} <span className="text-gray-500">({player.wins}П/{player.losses}П)</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="w-16 bg-gray-200 rounded-full h-2 mr-3">
                              <div
                                className="bg-green-500 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${player.winRate}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium text-gray-900">{player.winRate}%</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getRoleColor(player.bestRole)}`}>
                            {player.bestRole}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {player.lastPlayed}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'games' && (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-900">История игр</h2>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Дата
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Игроки
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Победитель
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Длительность
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        MVP
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {games.map((game) => (
                      <tr key={game.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {game.date}
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">
                            {game.players.join(', ')}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getWinnerColor(game.winner)}`}>
                            {getWinnerText(game.winner)}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {game.duration} мин
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <Star className="w-4 h-4 text-yellow-500 mr-1" />
                            <span className="text-sm text-gray-900">{game.mvp}</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'add-game' && (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-900">Добавить игру</h2>
            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Дата игры
                  </label>
                  <input
                    type="date"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Участники
                  </label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                    {players.map((player) => (
                      <label key={player.id} className="flex items-center space-x-2">
                        <input type="checkbox" className="rounded text-blue-600 focus:ring-blue-500" />
                        <span className="text-sm text-gray-700">{player.name}</span>
                      </label>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Победитель
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Выберите победителя</option>
                    <option value="mafia">Мафия</option>
                    <option value="civilians">Мирные жители</option>
                    <option value="neutral">Ничья</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Длительность (минуты)
                  </label>
                  <input
                    type="number"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="45"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    MVP игры
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Выберите MVP</option>
                    {players.map((player) => (
                      <option key={player.id} value={player.name}>{player.name}</option>
                    ))}
                  </select>
                </div>
                <div className="flex space-x-4 pt-4">
                  <button className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    Сохранить игру
                  </button>
                  <button className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium">
                    Отмена
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MafiaStatsApp;