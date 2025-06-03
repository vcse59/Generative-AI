import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, StatusBar, AppRegistry } from 'react-native';
import ChatbotUI from './components/ChatbotUI';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faWindowMinimize, faCircleXmark } from '@fortawesome/free-solid-svg-icons';

const App = () => {

  const [isChatVisible, setIsChatVisible] = useState(false);

  const toggleChatWindow = () => {
    setIsChatVisible(!isChatVisible);
  };

  return (
    <View style={styles.container}>
      <Text style={{ fontWeight: 'bold', fontSize: 30 }}>Welcome to ChatBot using Ollama models</Text>
      {isChatVisible && (
        <>
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
        </>
      )}
      <TouchableOpacity
        style={styles.chatButton}
        onPress={toggleChatWindow}
      >
        <Text style={styles.chatIcon}>💬</Text>
      </TouchableOpacity>
    </View>
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
  },
  chatIcon: {
    color: '#fff',
    fontSize: 24,
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1492c1', // Light background for the entire app
  },
  chatWindow: {
    position: 'fixed',
    bottom: 60,
    right: 60,
    height: 500,
    width: 350,
    backgroundColor: '#dae7ec', // Chat window color
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
    justifyContent: 'space-between', // Ensures space between title and actions
    padding: 5,
    backgroundColor: '#dae7ec', // Optional styling
  },
  chatTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    flex: 1, // Ensures the title takes up remaining space
  },
  chatHeaderActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  minimizeButton: {
    marginRight: 20, // Adds spacing between minimize and close buttons
    marginBottom: 20
  },
  closeButton: {
    // Additional button styling if needed
  }
});

export default App;