
import { useState, useRef, useEffect } from "react";
import "./Login.css";

function Login() {
  const [showPassword, setShowPassword] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const [cameraActive, setCameraActive] = useState(false);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [cameraError, setCameraError] = useState("");
  const [loginError, setLoginError] = useState("");

  // Start Camera
  const startCamera = async () => {
    try {
      setCameraError("");

      if (!navigator.mediaDevices?.getUserMedia) {
        setCameraError("Camera access is not supported by this browser.");
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" },
        audio: false,
      });

      streamRef.current = stream;
      setCameraActive(true);
    } catch (error) {
      console.error("Camera error:", error);
      setCameraError(
        "Unable to access camera. Please allow camera permission."
      );
    }
  };

  // Capture Photo
  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) {
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");

    if (!context || !canvas.width || !canvas.height) {
      setCameraError("Unable to capture photo. Please try again.");
      return;
    }

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    setCapturedPhoto(canvas.toDataURL("image/png"));

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setCameraActive(false);
  };

  // Retake Photo
  const retakePhoto = () => {
    setCapturedPhoto(null);
    setCameraError("");
    startCamera();
  };

  // Login Validation
  const handleLogin = (event) => {
    event.preventDefault();
    setLoginError("");

    const uniqueId = event.target.uniqueId.value.trim();
    const password = event.target.password.value;

    if (!uniqueId || !password) {
      setLoginError("Please enter your Unique ID and password.");
      return;
    }

    if (!capturedPhoto) {
      setLoginError("Please capture your live photo before continuing.");
      return;
    }

    setLoginError(
      "Your details are ready. Backend authentication is not connected yet."
    );
  };

  // Camera Preview
  useEffect(() => {
    if (cameraActive && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;

      videoRef.current.play().catch((error) => {
        console.error("Video playback error:", error);
        setCameraError("Unable to start camera preview.");
      });
    }
  }, [cameraActive]);

  // Stop Camera When Leaving Page
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }
    };
  }, []);

  return (
    <div className="login-container">

      {/* Left Welcome Section */}
      <div className="login-welcome">
        <div className="brand">
          <h1>IntelliTriage</h1>
          <span>SMARTER TRIAGE. BETTER CARE.</span>
        </div>

        <div className="welcome-content">
          <h2>Welcome to the Future of Clinical Triage</h2>
          <p>
            An intelligent clinical support system designed
            to assist healthcare professionals in patient
            assessment and triage.
          </p>
        </div>

        <div className="welcome-footer">
          Supporting healthcare professionals with intelligent technology.
        </div>
      </div>

      {/* Right Login Section */}
      <div className="login-section">
        <div className="login-box">

          <h2>Staff Login</h2>

          <p className="login-subtitle">
            Sign in to access your workspace
          </p>

          <form onSubmit={handleLogin}>

            <label>Unique IntelliTriage ID</label>

            <input
              type="text"
              name="uniqueId"
              placeholder="Enter your IntelliTriage ID"
              required
            />

            <label>Password</label>

            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Enter your password"
              required
            />

            <button
              type="button"
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? "Hide Password" : "Show Password"}
            </button>

            <div className="forgot-password">
              <a href="#">Forgot Password?</a>
            </div>

            {/* Live Photo Section */}
            <div className="login-camera">

              <label>Live Photo</label>

              {!capturedPhoto && !cameraActive && (
                <button
                  type="button"
                  onClick={startCamera}
                  className="camera-button"
                >
                  Start Camera
                </button>
              )}

              {cameraActive && (
                <>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="login-camera-preview"
                  />

                  <button
                    type="button"
                    onClick={capturePhoto}
                    className="camera-button"
                  >
                    Capture Photo
                  </button>
                </>
              )}

              {capturedPhoto && (
                <>
                  <img
                    src={capturedPhoto}
                    alt="Captured staff"
                    className="login-captured-photo"
                  />

                  <button
                    type="button"
                    onClick={retakePhoto}
                    className="camera-button"
                  >
                    Retake Photo
                  </button>
                </>
              )}

              <canvas ref={canvasRef} hidden />

              {cameraError && (
                <p className="camera-error">{cameraError}</p>
              )}

            </div>

            {/* Login Validation Message */}
            {loginError && (
              <p className="login-error">
                {loginError}
              </p>
            )}

            <button type="submit">
              Sign In
            </button>

          </form>

          <p className="login-note">
            Secure access for authorized healthcare staff
          </p>

        </div>
      </div>

    </div>
  );
}

export default Login;
