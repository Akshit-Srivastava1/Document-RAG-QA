import { useEffect, useRef, useState } from "react";
import { askQuestion } from "../services/api";
import Message from "./Message";
import Loader from "./Loader";
import "./Chat.css";

function Chat() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages, loading]);

    const handleAsk = async () => {
        if (!question.trim() || loading) return;
        const currentQuestion = question.trim();
        setMessages((prev) => [
            ...prev,
            {
                type: "user",
                text: currentQuestion,
            },
        ]);

        setQuestion("");
        setLoading(true);
        try {
            const response = await askQuestion(currentQuestion);
            setMessages((prev) => [
                ...prev,
                {
                    type: "bot",
                    text: response.answer,
                    pages: response.source_pages,
                },
            ]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                {
                    type: "bot",
                    text:
                        error.response?.data?.detail ||
                        "Unable to generate an answer.",
                    pages: [],
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === "Enter") {
            handleAsk();
        }
    };

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.length === 0 && (
                    <div className="empty-chat">
                        💬 Ask questions from your uploaded PDF.
                    </div>
                )}
                {messages.map((message, index) => (
                    <Message key={index} type={message.type}text={message.text} pages={message.pages}/>
                ))}

                {loading && (
                    <Loader text="Generating answer..." />
                )}

                <div ref={messagesEndRef}></div>
            </div>

            <div className="chat-input">
                <input
                    type="text"
                    placeholder="Ask anything from the document..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={loading}
                />

                <button onClick={handleAsk} disabled={loading}>
                    {loading ? "..." : "Ask"}
                </button>
            </div>
        </div>
    );
}

export default Chat;