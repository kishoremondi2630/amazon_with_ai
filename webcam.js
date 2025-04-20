import React, { useState, useRef, useEffect } from "react";
import * as faceapi from "face-api.js";

const CameraComponent = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [capturedImages, setCapturedImages] = useState([]);

  useEffect(() => {
    startCamera();
    loadModels();
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error("Error accessing camera:", error);
    }
  };

  const loadModels = async () => {
    await faceapi.nets.tinyFaceDetector.loadFromUri("/models");
    await faceapi.nets.faceLandmark68Net.loadFromUri("/models");
    await faceapi.nets.faceRecognitionNet.loadFromUri("/models");
    console.log("Face API models loaded");
  };

  const detectFace = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks();

    if (detections.length > 0) {
      const context = canvas.getContext("2d");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.clearRect(0, 0, canvas.width, canvas.height);
      faceapi.draw.drawDetections(canvas, detections);
      faceapi.draw.drawFaceLandmarks(canvas, detections);
    }
  };

  const captureImage = () => {
    const canvas = document.createElement("canvas");
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageUrl = canvas.toDataURL("image/png");
    setCapturedImages([...capturedImages, imageUrl]);
  };

  return (
    <div>
      <video ref={videoRef} autoPlay onPlay={detectFace} style={{ width: "100%" }} />
      <canvas ref={canvasRef} style={{ position: "absolute", top: 0, left: 0 }} />
      <button onClick={captureImage}>Capture</button>
      <div>
        {capturedImages.map((img, index) => (
          <img key={index} src={img} alt={`Captured ${index}`} style={{ width: "100px", margin: "5px" }} />
        ))}
      </div>
    </div>
  );
};

export default CameraComponent;
