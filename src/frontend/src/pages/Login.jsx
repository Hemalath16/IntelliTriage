
import { useState } from "react";
import "./Login.css";

function Login() {
    const [showPassword, setShowPassword] = useState(false);
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

          <form>
            <label>Unique IntelliTriage ID</label>
<input
  type="text"
  placeholder="Enter your IntelliTriage ID"
  required
/>

            <input
  type={showPassword ? "text" : "password"}
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

            <button type="submit">Sign In</button>
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
