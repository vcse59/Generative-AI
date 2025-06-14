import React, { useState, useRef } from 'react';
import {
    StyleSheet,
    View,
    TextInput,
    ScrollView,
    KeyboardAvoidingView,
    Platform,
    Keyboard,
    TouchableOpacity,
    useWindowDimensions,
} from 'react-native';
import RenderHTML from 'react-native-render-html';
import { OLLAMA_LLM_MODEL_NAME } from '@env';

const ChatbotUI = ({ microserviceHost }) => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const scrollViewRef = useRef();
    const inputRef = useRef(null);
    const { width } = useWindowDimensions();
    const MarkdownIt = require('markdown-it');
    const md = new MarkdownIt();

    // Process user query and fetch response
    async function processUserQuery(prompt) {
        try {
            const response = await fetch(`http://${microserviceHost}:8000/generate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            const htmlResponse = md.render(data.response) || "Please try again";
            const citationLinks = data.citation_links.map(link => {
                return `<a href="${link.url}" target="_blank">${link.title}</a>`;
            }).join('<br />'); // Join all citation links with a line break

            // Combine response and citations
            const fullResponse = `${htmlResponse}<br /><strong>Citations:</strong><br />${citationLinks}`;

            setMessages((prevMessages) => [
                ...prevMessages,
                {
                    id: Date.now(),
                    text: fullResponse,
                    sender: 'bot',
                }
            ]);
        } catch (error) {
            console.error("Error fetching response:", error);
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
        inputRef.current?.focus();
    };

    const renderMessage = (item) => (
        <View
            key={item.id}
            style={[
                styles.messageContainer,
                item.sender === 'user' ? styles.userMessage : styles.botMessage,
            ]}
        >
            {item.sender === 'bot' ? (
                <RenderHTML contentWidth={width} source={{ html: item.text }} />
            ) : (
                <View>
                    <RenderHTML contentWidth={width} source={{ html: `<p>${item.text}</p>` }} />
                </View>
            )}
        </View>
    );

    return (
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
                    placeholder="Type your message..."
                    multiline={false}
                    placeholderTextColor="#aaa"
                />
                <TouchableOpacity onPress={handleSendMessage}>
                    <View style={styles.sendButton}>
                        <RenderHTML contentWidth={50} source={{ html: "<strong>Send</strong>" }} />
                    </View>
                </TouchableOpacity>
            </View>
        </KeyboardAvoidingView>
    );
};

const styles = StyleSheet.create({
    chatContainer: {
        flex: 1,
    },
    messagesContainer: {
        flex: 1,
        paddingHorizontal: 10,
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
    botMessage: {
        backgroundColor: '#30b5e7',
        alignSelf: 'flex-end',
    },
    userMessage: {
        backgroundColor: '#73c4e2',
        alignSelf: 'flex-start',
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 10,
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
        paddingHorizontal: 15,
        paddingVertical: 8,
        borderRadius: 10,
    },
});

export default ChatbotUI;