import React, { useState, useEffect } from "react";
import ChatInterface from "./components/ChatInterface";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import { healthAPI } from "./services/api";

function App() {
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      await healthAPI.checkHealth();
      setIsConnected(true);
    } catch (error) {
      console.error("Failed to connect to backend:", error);
      setIsConnected(false);
    }
  };

  if (isConnected === null) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Connecting to server...</p>
        </div>
      </div>
    );
  }

  if (isConnected === false) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <strong className="font-bold">Connection Error!</strong>
            <span className="block sm:inline">
              {" "}
              Unable to connect to the backend server.
            </span>
          </div>
          <p className="text-gray-600 mb-4">
            Please make sure the FastAPI backend is running on{" "}
            <code className="bg-gray-100 px-2 py-1 rounded">
              http://localhost:8000
            </code>
          </p>
          <button onClick={checkConnection} className="btn btn-primary">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onMenuClick={() => setSidebarOpen(true)} />

      <div className="flex">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <main className="flex-1">
          <ChatInterface />
        </main>
      </div>
    </div>
  );
}

export default App;
