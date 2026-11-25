
import {
  Activity,
  ArrowRight,
  HeartPulse,
  ShieldCheck,
  Stethoscope,
  ClipboardList,
  Users,
  Menu
} from "lucide-react";

import { Link } from "react-router-dom";
import "./Landing.css";

function Landing() {
  return (
    <div className="landing-page">

      {/* NAVIGATION BAR */}
      <nav className="navbar">
        <div className="landing-logo">
          <div className="logo-icon">
            <Activity size={27} />
          </div>
          <span>IntelliTriage</span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#features">Features</a>
          <a href="#workflow">How It Works</a>
        </div>

        <div className="nav-actions">
          
<Link to="/login" className="login-link">
  Login <ArrowRight size={16} />
</Link>

          <Link to="/register" className="register-btn">
            Register <ArrowRight size={16} />
          </Link>
        </div>

        <button className="mobile-menu" aria-label="Open menu">
          <Menu />
        </button>
      </nav>

      {/* HERO SECTION */}
      <section className="hero-section" id="home">

        <div className="hero-content">
          <span className="hero-tag">
            <Activity size={16} />
            INTELLIGENT HEALTHCARE TECHNOLOGY
          </span>

          <h1>
            Smarter Triage.
            <span> Better Care.</span>
          </h1>

          <p>
            Introducing IntelliTriage, an AI-based clinical
            triage assistant designed to support healthcare
            professionals in patient assessment and
            clinical decision-making.
          </p>

          <div className="hero-buttons">
            <Link to="/register" className="primary-btn">
              Get Started <ArrowRight size={19} />
            </Link>

            <a href="#about" className="secondary-btn">
              Explore More
            </a>
          </div>

          <div className="hero-trust">
            <ShieldCheck size={20} />
            Supporting healthcare professionals
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-circle">
            <HeartPulse size={105} strokeWidth={1.3} />
          </div>

          <div className="floating-card card-one">
            <ClipboardList size={25} />
            <div>
              <strong>Patient Assessment</strong>
              <small>Structured information</small>
            </div>
          </div>

          <div className="floating-card card-two">
            <Stethoscope size={25} />
            <div>
              <strong>Clinical Support</strong>
              <small>Decision assistance</small>
            </div>
          </div>

          <div className="floating-card card-three">
            <ShieldCheck size={24} />
            <div>
              <strong>Healthcare Focused</strong>
              <small>Professional support</small>
            </div>
          </div>
        </div>

      </section>

      {/* ABOUT SECTION */}
      <section className="about-section" id="about">
        <span className="section-tag">ABOUT INTELLITRIAGE</span>

        <h2>
          Bringing Intelligence Into
          <span> Patient Triage</span>
        </h2>

        <p>
          IntelliTriage aims to simplify the patient triage
          process through intelligent technology. It helps
          healthcare professionals organize patient
          information, assess symptoms and review
          clinical decision-support information.
        </p>
      </section>

      {/* FEATURES SECTION */}
      <section className="features-section" id="features">

        <div className="section-heading">
          <span className="section-tag">OUR FEATURES</span>
          <h2>Designed for Better Healthcare</h2>
          <p>
            Supporting healthcare professionals throughout
            the patient assessment process.
          </p>
        </div>

        <div className="feature-grid">

          <div className="feature-card">
            <div className="feature-icon">
              <Users size={30} />
            </div>
            <h3>Patient Management</h3>
            <p>
              Organized patient registration and
              information management.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <Activity size={30} />
            </div>
            <h3>Symptom Assessment</h3>
            <p>
              Structured collection of patient symptoms
              and assessment details.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <HeartPulse size={30} />
            </div>
            <h3>Intelligent Triage Support</h3>
            <p>
              AI-based support to assist clinical
              assessment and decision-making.
            </p>
          </div>

        </div>
      </section>

      {/* WORKFLOW SECTION */}
      <section className="workflow-section" id="workflow">
        <div className="section-heading">
          <span className="section-tag">OUR WORKFLOW</span>
          <h2>How IntelliTriage Works</h2>
        </div>

        <div className="workflow-grid">

          <div className="workflow-card">
            <span>01</span>
            <h3>Patient Registration</h3>
            <p>Record essential patient information.</p>
          </div>

          <div className="workflow-card">
            <span>02</span>
            <h3>Patient Assessment</h3>
            <p>Collect symptoms, vital signs and history.</p>
          </div>

          <div className="workflow-card">
            <span>03</span>
            <h3>Triage Support</h3>
            <p>Review AI-generated clinical support results.</p>
          </div>

          <div className="workflow-card">
            <span>04</span>
            <h3>Clinical Review</h3>
            <p>Doctor reviews and approves the assessment.</p>
          </div>

        </div>
      </section>

      {/* FOOTER */}
      <footer className="landing-footer">
        <div className="footer-brand">
          <Activity size={27} />
          <h2>IntelliTriage</h2>
        </div>

        <p>
          Smarter Triage. Better Care.
        </p>

        <small>
          IntelliTriage is a clinical decision-support
          system and does not replace professional
          medical judgement.
        </small>

        <div className="footer-bottom">
          © 2026 IntelliTriage. All rights reserved.
        </div>
      </footer>

    </div>
  );
}

export default Landing;
