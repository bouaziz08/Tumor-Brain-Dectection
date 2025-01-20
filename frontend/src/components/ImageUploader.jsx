import React, { useState } from "react";
import axios from "axios";

function ImageUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      alert("Veuillez sélectionner une image !");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

    } catch (error) {
      console.error("Erreur lors de l'envoi de l'image :", error);
      setResult("Une erreur s'est produite. Veuillez réessayer.");
    }
  };

  const fetchTumor = async () => {
    try {

      const response = await axios.get("http://localhost:8000/predict");
      setResult(response.data || "Pas de résultat trouvé.");
    } catch (error) {
        console.error("Erreur lors de la récupération des prédictions :", error);
        setResult("Une erreur s'est produite lors de la récupération des données.");
    }
  };

  return (
    <div>
      <h1>Détection de tumeurs</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="image/*" />
        <button type="submit">upload</button>
      </form><br/>
      <button onClick={fetchTumor}>Obtenir le résultat de la prédiction</button>

      {result && <p>{result}</p>}
    </div>
  );
}

export default ImageUploader;
