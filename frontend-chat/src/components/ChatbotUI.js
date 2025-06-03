import React, { useState, useEffect, useRef } from 'react';
import {
    StyleSheet,
    View,
    Text,
    TextInput,
    ScrollView,
    KeyboardAvoidingView,
    Platform,
    Keyboard,
    TouchableOpacity,
} from 'react-native';

const ChatbotUI = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const scrollViewRef = useRef();
    const inputRef = useRef(null);

    async function processUserQuery(prompt) {
        try {
            const response = await fetch("http://127.0.0.1:8000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ model_name: "phi", prompt: prompt })
            });

            // Check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();  // Correctly parse JSON
            const combinedResponse = data.response || "Please try again"; // Ensure a fallback if empty

            if (combinedResponse.length == 0) {
                return getFalconResponse(prompt);
            }

            // Update the message UI progressively with each chunk
            setMessages((prevMessages) => [
                ...prevMessages,
                {
                    id: Date.now(),
                    text: combinedResponse,
                    sender: 'bot',
                }
            ]);

        } catch (error) {
            console.error("Error fetching Falcon response:", error);
        }
    }


    const handleSendMessage = async () => {
        if (inputMessage.trim() === '') return;

        const userQuery = {
            id: Date.now(),
            text: inputMessage.trim(),
            sender: 'user',
        };

        try {
            setMessages((prevMessages) => [...prevMessages, userQuery]);
            setInputMessage("");
            await processUserQuery(inputMessage);
        } catch (error) {
            console.error('Error sending message:', error);
        }

        Keyboard.dismiss();

        if (inputRef.current) {
            inputRef.current.focus();
        }
    };

    const renderMessage = (item) => {
        return (
            <View
                key={item.id}
                style={[
                    styles.messageContainer,
                    item.sender === 'user' ? styles.userMessage : styles.botMessage,
                ]}
            >
                <Text>{item.text}</Text>
            </View>
        );
    };

    const handleKeyPress = (e) => {
        if (e.nativeEvent.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={styles.chatContainer}
            >
                <ScrollView
                    ref={scrollViewRef}
                    onContentSizeChange={() =>
                        scrollViewRef.current.scrollToEnd({ animated: true })
                    }
                    style={styles.messagesContainer}
                >
                    {messages.map(renderMessage)}
                </ScrollView>

                <View style={styles.inputContainer}>
                    <TextInput
                        ref={inputRef}
                        style={styles.input}
                        value={inputMessage}
                        onChangeText={setInputMessage}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your message..."
                        multiline={false}
                        numberOfLines={4}
                        textAlignVertical="auto"
                        placeholderTextColor="#aaa"
                    />
                    <TouchableOpacity onPress={handleSendMessage}>
                        <Text style={styles.sendButton}>Send</Text>
                    </TouchableOpacity>
                </View>
            </KeyboardAvoidingView>
        </>
    );
};

const styles = StyleSheet.create({
    chatContainer: {
        flex: 1,
    },
    messagesContainer: {
        flex: 1,
    },
    messageContainer: {
        maxWidth: '80%',
        padding: 10,
        marginBottom: 10,
        borderRadius: 10,
        borderWidth: 1,
        borderColor: 'black',
        backgroundColor: 'white',
        shadowColor: 'black',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    userMessage: {
        backgroundColor: '#30b5e7',
        alignSelf: 'flex-start',
    },
    botMessage: {
        backgroundColor: '#73c4e2',
        alignSelf: 'flex-end',
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'flex-end',
    },
    input: {
        flex: 1,
        padding: 10,
        borderRadius: 20,
        backgroundColor: '#fff',
        marginRight: 10,
    },
    sendButton: {
        backgroundColor: '#0078d4',
        color: '#fff',
        paddingHorizontal: 15,
        paddingVertical: 8,
        borderRadius: 10,
    },
});

export default ChatbotUI;