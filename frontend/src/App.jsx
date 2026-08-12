import { useState } from "react";
import Navbar from "./components/Navbar";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import "./App.css";

function App() {
    const [uploaded, setUploaded] = useState(false);
    const handleUploadSuccess = () => {
        setUploaded(true);
    };

    return (
        <div className="app">
            <Navbar/>
            <div className="container">
                <Upload onUploadSuccess={handleUploadSuccess}/>
                {
                    uploaded ? (
                        <Chat/>
                    ) : (
                        <div className="welcome-card">
                            <h2>Welcome 👋</h2>
                            <p>
                                Upload a PDF document to start asking
                                questions using Retrieval-Augmented
                                Generation (RAG).
                            </p>
                        </div>
                    )
                }
            </div>
        </div>
    );
}

export default App;