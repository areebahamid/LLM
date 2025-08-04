import React from "react";
import { Menu, Bot, Wifi, WifiOff } from "lucide-react";

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <button
            onClick={onMenuClick}
            className="p-2 rounded-md hover:bg-gray-100 lg:hidden"
            aria-label="Open menu">
            <Menu className="h-5 w-5" />
          </button>

          <div className="flex items-center space-x-2">
            <Bot className="h-6 w-6 text-primary-600" />
            <h1 className="text-xl font-semibold text-gray-900">
              Student LLM Assistant
            </h1>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Wifi className="h-4 w-4 text-green-500" />
            <span>Connected</span>
          </div>

          <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Ollama Ready</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
