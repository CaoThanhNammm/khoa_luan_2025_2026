import React, { useState } from 'react';
import ChatService from '../../services/ChatService';
import { useAuth } from '../../context/AuthContext';

const ApiDebugger: React.FC = () => {
  const { user } = useAuth();
  const [logs, setLogs] = useState<string[]>([]);
  const [conversationId, setConversationId] = useState<string>('');

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${timestamp}] ${message}`]);
  };

  const testCreateStudentHandbookConversation = async () => {
    try {
      addLog('🚀 Testing: Create conversation with student handbook...');
      const conversation = await ChatService.startNewConversationWithDocument(
        'Lịch sử trường đại học nông lâm tphcm',
        'so_tay_sinh_vien_2024'
      );
      setConversationId(conversation.id);
      addLog(`✅ Success: Conversation created with ID: ${conversation.id}`);
      addLog(`📝 Response: ${JSON.stringify(conversation, null, 2)}`);
    } catch (error) {
      addLog(`❌ Error: ${error}`);
    }
  };

  const testSendStsvMessage = async () => {
    if (!conversationId) {
      addLog('❌ Error: No conversation ID. Create conversation first.');
      return;
    }

    try {
      addLog('🚀 Testing: Send message using STSV API...');
      const message = await ChatService.sendMessageStsv(
        conversationId,
        'Địa chỉ trường đại học nông lâm tphcm'
      );
      addLog(`✅ Success: Message sent via STSV API`);
      addLog(`📝 Response: ${JSON.stringify(message, null, 2)}`);
    } catch (error) {
      addLog(`❌ Error: ${error}`);
    }
  };

  const testSendRegularMessage = async () => {
    if (!conversationId) {
      addLog('❌ Error: No conversation ID. Create conversation first.');
      return;
    }

    try {
      addLog('🚀 Testing: Send message using regular API...');
      const message = await ChatService.sendMessage(
        conversationId,
        'Test regular message'
      );
      addLog(`✅ Success: Message sent via regular API`);
      addLog(`📝 Response: ${JSON.stringify(message, null, 2)}`);
    } catch (error) {
      addLog(`❌ Error: ${error}`);
    }
  };

  const testGetConversation = async () => {
    if (!conversationId) {
      addLog('❌ Error: No conversation ID. Create conversation first.');
      return;
    }

    try {
      addLog('🚀 Testing: Get conversation details...');
      const conversation = await ChatService.getConversation(conversationId);
      addLog(`✅ Success: Conversation retrieved`);
      addLog(`📝 Messages count: ${conversation.messages.length}`);
      addLog(`📝 Has document: ${conversation.hasDocument}`);
      addLog(`📝 Document ID: ${conversation.documentInfo?.documentId}`);
    } catch (error) {
      addLog(`❌ Error: ${error}`);
    }
  };

  const clearLogs = () => {
    setLogs([]);
  };

  if (!user) {
    return (
      <div className="p-4 bg-red-100 text-red-800 rounded">
        Please login to use API debugger
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-slate-800 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
        Student Handbook API Debugger
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <button
          onClick={testCreateStudentHandbookConversation}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          1. Create STSV Conversation
        </button>
        
        <button
          onClick={testSendStsvMessage}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
          disabled={!conversationId}
        >
          2. Send STSV Message
        </button>
        
        <button
          onClick={testSendRegularMessage}
          className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition-colors"
          disabled={!conversationId}
        >
          3. Send Regular Message
        </button>
        
        <button
          onClick={testGetConversation}
          className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
          disabled={!conversationId}
        >
          4. Get Conversation
        </button>
      </div>

      <div className="mb-4 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">
          API Logs
        </h3>
        <button
          onClick={clearLogs}
          className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600 transition-colors"
        >
          Clear Logs
        </button>
      </div>

      <div className="bg-gray-100 dark:bg-slate-700 rounded-lg p-4 h-96 overflow-y-auto">
        {logs.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400">No logs yet. Click buttons above to test APIs.</p>
        ) : (
          <div className="space-y-2">
            {logs.map((log, index) => (
              <div
                key={index}
                className="text-sm font-mono text-gray-800 dark:text-gray-200 whitespace-pre-wrap"
              >
                {log}
              </div>
            ))}
          </div>
        )}
      </div>

      {conversationId && (
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
          <p className="text-sm text-blue-800 dark:text-blue-200">
            <strong>Current Conversation ID:</strong> {conversationId}
          </p>
        </div>
      )}
    </div>
  );
};

export default ApiDebugger;