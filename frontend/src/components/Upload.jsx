import { useState } from "react";
import { uploadPDF } from "../services/api";
import "./Upload.css";

function Upload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;
        if (selectedFile.type !== "application/pdf") {
            setError("Only PDF files are allowed.");
            setFile(null);
            return;
        }
        setError("");
        setMessage("");
        setFile(selectedFile);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a PDF.");
            return;
        }
        try {
            setLoading(true);
            const response = await uploadPDF(file);
            setMessage(response.message);
            if (onUploadSuccess) {
                onUploadSuccess(response);
            }

        } catch (err) {
            setError(
                err.response?.data?.detail ||
                "Upload failed."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-card">
            <h2>📄 Upload PDF</h2>
            <p>
                Upload a PDF document to start asking questions.
            </p>
            <input type="file" accept=".pdf" onChange={handleFileChange}/>
            {
                file && (
                    <p className="filename">
                        📎 {file.name}
                    </p>
                )
            }

            <button onClick={handleUpload} disabled={loading}>
                {
                    loading
                        ? "Uploading..."
                        : "Upload PDF"
                }
            </button>
            {
                message && (
                    <p className="success">
                        {message}
                    </p>
                )
            }

            {
                error && (
                    <p className="error">
                        {error}
                    </p>
                )
            }
        </div>
    );
}

export default Upload;