import "./Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="logo">
                    🤖
                </div>
                <div className="title-section">
                    <h1>Document RAG QA</h1>
                    <p>FastAPI • ChromaDB • Gemini • RAG</p>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;