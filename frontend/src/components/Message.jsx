import "./Message.css";

function Message({ type, text, pages }) {
    return (
        <div className={`message ${type}`}>
            <div className="message-header">
                <span className="avatar">
                    {type === "user" ? "👤" : "🤖"}
                </span>

                <span className="sender">
                    {type === "user" ? "You" : "AI Assistant"}
                </span>
            </div>

            <div className="message-content">
                {text}
            </div>
            {type === "bot" && pages && pages.length > 0 && (
                    <div className="source-pages">
                        <strong>Source Pages:</strong>
                        {pages.map((page) => (
                            <span key={page} className="page-badge">
                                {page}
                            </span>
                        ))}
                    </div>
                )}
        </div>
    );
}

export default Message;