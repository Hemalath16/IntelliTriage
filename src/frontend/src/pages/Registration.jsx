
import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { Activity, ArrowRight, UserRound } from "lucide-react";
import "./Registration.css";

function Registration() {

  
  const videoRef = useRef(null);
const canvasRef = useRef(null);
const streamRef = useRef(null);

  const [cameraActive, setCameraActive] = useState(false);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [photoError, setPhotoError] = useState("");
  const [cameraError, setCameraError] = useState("");

  useEffect(() => {
  return () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  };
}, []);


const startCamera = async () => {
  try {
    setCameraError("");

    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user" },
      audio: false,
    });

    streamRef.current = stream;

    if (videoRef.current) {
      videoRef.current.srcObject = stream;
      await videoRef.current.play();
      setCameraActive(true);
    } else {
      stream.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  } catch (error) {
    console.error("Camera error:", error);

    setCameraError(
      "Unable to access camera. Please allow camera permission."
    );
  }
};





const capturePhoto = () => {
  if (!videoRef.current || !canvasRef.current) return;

  const video = videoRef.current;
  const canvas = canvasRef.current;

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const context = canvas.getContext("2d");

  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const photo = canvas.toDataURL("image/jpeg");

  setCapturedPhoto(photo);

  video.srcObject?.getTracks().forEach((track) => track.stop());

  setCameraActive(false);
};


const retakePhoto = () => {
  setCapturedPhoto(null);
  setCameraError("");
  startCamera();
};





  const [role, setRole] = useState("Receptionist");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState("");

  const handleSubmit = (e) => {
  e.preventDefault();

  setPasswordError("");
  setPasswordSuccess("");
  setPhotoError("");

  if (!capturedPhoto) {
  setPhotoError("Please capture your live photo before submitting.");
  return;
}

  if (password !== confirmPassword) {
    setPasswordError("Passwords do not match. Please try again.");
    return;
  }

  setPasswordSuccess("Passwords match successfully!");
};

  return (
    <div className="registration-page">

      <div className="registration-header">
        <Link to="/" className="registration-logo">
          <Activity size={30} />
          <span>IntelliTriage</span>
        </Link>

        <p>Already have an account? <Link to="/login">Login</Link></p>
      </div>

      <div className="registration-container">

        <div className="registration-heading">
          <div className="registration-icon">
            <UserRound size={30} />
          </div>

          <h1>Create Your Account</h1>
          <p>Join IntelliTriage healthcare professionals.</p>
        </div>

        <form
  className="registration-form"
  onSubmit={handleSubmit}
  noValidate={false}
>

          <h3>Personal Information</h3>

          <label>Full Name</label>
          <input
  type="text"
  placeholder="Enter your full name"
  required
  minLength={3}
/>

          <div className="registration-row">
            <div>
              <label>Age</label>
              <input
  type="number"
  placeholder="Enter your age"
  required
  min="18"
  max="100"
/>
            </div>

            <div>
              <label>Phone Number</label>
              <input
  type="tel"
  placeholder="Enter phone number"
  required
  pattern="[0-9]{10}"
  maxLength={10}
  title="Please enter a valid 10-digit phone number"
/>
            </div>
          </div>

          <label>Email Address</label>
          <input
  type="email"
  placeholder="Enter your email"
  required
/>



<h3>Live Photo Verification</h3>

<div className="camera-section">

  {capturedPhoto ? (
    <img
      src={capturedPhoto}
      alt="Captured registration photo"
      className="captured-photo"
    />
  ) : (
    <video
      ref={videoRef}
      autoPlay
      playsInline
      muted
      className="camera-preview"
    />
  )}

  <canvas ref={canvasRef} style={{ display: "none" }} />

  {!cameraActive && !capturedPhoto && (
    <button
      type="button"
      onClick={startCamera}
      className="camera-button"
    >
      Open Camera
    </button>
  )}

  {cameraActive && (
    <button
      type="button"
      onClick={capturePhoto}
      className="camera-button"
    >
      Capture Photo
    </button>
  )}

  {capturedPhoto && (
    <button
      type="button"
      onClick={retakePhoto}
      className="camera-button"
    >
      Retake Photo
    </button>
  )}

  {cameraError && (
    <p className="camera-error">{cameraError}</p>
  )}

  {photoError && (
  <p className="camera-error">{photoError}</p>
)}



</div>


          <h3>Professional Information</h3>

          <label>Select Your Role</label>
          
<select
  value={role}
  onChange={(e) => setRole(e.target.value)}
>
  <option value="Receptionist">Receptionist</option>
  <option value="Nurse">Nurse</option>
  <option value="Doctor">Doctor</option>
  <option value="Admin">Admin</option>
</select>

{role === "Admin" && (
  <p className="registration-note">
    Admin accounts require authorised provisioning
    or an approved invitation.
  </p>
)}


          {(role === "Nurse" || role === "Doctor") && (
            <>
              <label>Qualification</label>
<input
  type="text"
  placeholder="Enter your qualification"
  required
  minLength={2}
/>

              <label>Professional Registration Number</label>
<input
  type="text"
  placeholder="Enter registration number"
  required
  minLength={3}
/>
            </>
          )}






          <h3>Account Security</h3>

          <label>Password</label>
          <input
  type="password"
  placeholder="Create a password"
  required
  minLength={8}
  value={password}
  onChange={(e) => setPassword(e.target.value)}
/>

          <label>Confirm Password</label>
          <input
  type="password"
  placeholder="Confirm your password"
  required
  minLength={8}
  value={confirmPassword}
  onChange={(e) => setConfirmPassword(e.target.value)}
/>

{passwordError && (
  <p className="camera-error">
    {passwordError}
  </p>
)}


{passwordSuccess && (
  <p className="password-success">
    {passwordSuccess}
  </p>
)}

          <button type="submit" className="registration-submit">
            Submit Registration <ArrowRight size={18} />
          </button>

          <p className="registration-note">
            Account access is subject to the required verification
            and approval process.
          </p>

        </form>
      </div>
    </div>
  );
}

export default Registration;
