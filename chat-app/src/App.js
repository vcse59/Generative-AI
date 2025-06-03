import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import ChatbotUI from './components/ChatbotUI';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faWindowMinimize, faCircleXmark } from '@fortawesome/free-solid-svg-icons';

const HEALTH_API_URL = 'http://127.0.0.1:8000/health';

const App = () => {
  const [isChatVisible, setIsChatVisible] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [healthStatus, setHealthStatus] = useState('checking'); // 'checking', 'ok', 'fail'
  const [healthText, setHealthText] = useState(''); // 'checking', 'ok', 'fail'
  const [healthColor, setHealthColor] = useState('#888'); // 'checking', 'ok', 'fail'

  const toggleChatWindow = () => {
    setIsChatVisible(!isChatVisible);
  };

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(HEALTH_API_URL, { method: 'GET', headers: { "Content-Type": "application/json" } });
        const data = await res.json();
        console.log("Health check response JSON:", data.status);
        if (data.status === 'healthy') {
          setHealthStatus('ok');
          setIsInitialized(true);
          setHealthColor('green');
          setIsInitialized(true);
        } else if (data.status === 'wait') {
          setHealthStatus('wait');
          setHealthColor('orange');
          setIsInitialized(false);
        } else if(data.status === 'error') {
          setHealthStatus('error');
          setHealthColor('purple');
          setIsInitialized(false);
        }else {
          setHealthStatus('fail');
          setHealthColor('red');
          setIsInitialized(false);
        }
        setHealthText(data.message);
      } catch (e) {
        setHealthStatus('fail');
        setHealthText('Backend service is not available');
        setHealthColor('red');
        setIsInitialized(false);
      }
    };

    checkHealth();
    // Optionally, poll every 30s:
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <View style={styles.container}>
        <Text style={{ fontWeight: 'bold', fontSize: 22, alignContent: 'center' }}>
          Welcome to chat app based on mcp client and server implementation (E2E)
        </Text>
        <Text style={{ marginTop: 20, marginBottom: 10, color: healthColor, fontWeight: 'bold' , fontSize: 28 }}>
          {healthText}
        </Text>

        {isChatVisible && isInitialized && (
          <View style={styles.chatWindow}>
            <View style={styles.chatHeader}>
              <Text style={styles.chatTitle}>Chat with Us</Text>
              <View style={styles.chatHeaderActions}>
                <TouchableOpacity onPress={toggleChatWindow} style={styles.minimizeButton}>
                  <FontAwesomeIcon icon={faWindowMinimize} size={30} color="black" />
                </TouchableOpacity>
                <TouchableOpacity onPress={toggleChatWindow} style={styles.closeButton}>
                  <FontAwesomeIcon icon={faCircleXmark} size={30} color="black" />
                </TouchableOpacity>
              </View>
            </View>
            <ChatbotUI />
          </View>
        )}

        {/* Button to open chat */}
        <TouchableOpacity
          style={[
            styles.chatButton,
            healthStatus !== 'ok' && styles.chatButtonDisabled
          ]}
          onPress={toggleChatWindow}
          disabled={healthStatus !== 'ok'}
        >
          <Text style={styles.chatIcon}>💬</Text>
        </TouchableOpacity>
      </View>
    </>
  );
};

const styles = StyleSheet.create({
  chatButton: {
    position: 'fixed',
    bottom: 20,
    right: 20,
    backgroundColor: '#0078d4',
    padding: 10,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    opacity: 1,
  },
  chatButtonDisabled: {
    backgroundColor: '#aaa',
    opacity: 0.5,
  },
  chatIcon: {
    color: '#fff',
    fontSize: 24,
  },
  container: {
    flex: 1,
    marginTop: '2rem',
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: '#1492c1',
  },
  chatWindow: {
    position: 'fixed',
    bottom: 60,
    right: 60,
    height: 500,
    width: 400,
    backgroundColor: '#dae7ec',
    borderRadius: 15,
    padding: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.2,
    shadowRadius: 5,
  },
  chatHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 5,
    backgroundColor: '#dae7ec',
  },
  chatTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    flex: 1,
  },
  chatHeaderActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  minimizeButton: {
    marginRight: 20,
    marginBottom: 30,
  },
  updateKnowledgeSourceButton: {
    backgroundColor: '#0078d4',
    padding: 10,
    justifySelf: 'flex-start',
    borderRadius: 5,
    marginBottom: 20,
    marginTop: '12rem',
  },
  updateText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  closeButton: {
    marginBottom: 20,
  },
});

export default App;
