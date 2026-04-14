import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  Shield,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Validation
    if (!form.username || !form.email || !form.password || !form.confirmPassword) {
      setError("Please fill in all fields");
      return;
    }
    if (form.username.length < 3) {
      setError("Username must be at least 3 characters");
      return;
    }
    if (form.password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }
    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      await register({
        username: form.username,
        email: form.email,
        password: form.password,
      });
      setSuccess("Account created successfully! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      const msg =
        err.response?.data?.detail || "Registration failed. Please try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-layout">
      <div className="auth-container">
        <div className="card">
          {/* Branding */}
          <div className="brand">
            <div className="brand-icon">
              <Shield />
            </div>
            <h1>FinShield</h1>
            <p>Create your secure account</p>
          </div>

          {/* Alerts */}
          {error && (
            <div className="alert alert-error">
              <AlertCircle size={16} />
              {error}
            </div>
          )}
          {success && (
            <div className="alert alert-success">
              <CheckCircle2 size={16} />
              {success}
            </div>
          )}

          {/* Register form */}
          <form onSubmit={handleSubmit} id="register-form">
            <div className="form-group">
              <label className="form-label" htmlFor="reg-username">
                Username
              </label>
              <div className="input-wrapper">
                <input
                  id="reg-username"
                  name="username"
                  type="text"
                  className="form-input"
                  placeholder="Choose a username"
                  value={form.username}
                  onChange={handleChange}
                  autoComplete="username"
                />
                <User className="input-icon" />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="reg-email">
                Email Address
              </label>
              <div className="input-wrapper">
                <input
                  id="reg-email"
                  name="email"
                  type="email"
                  className="form-input"
                  placeholder="you@example.com"
                  value={form.email}
                  onChange={handleChange}
                  autoComplete="email"
                />
                <Mail className="input-icon" />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="reg-password">
                Password
              </label>
              <div className="input-wrapper">
                <input
                  id="reg-password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  className="form-input"
                  placeholder="Min. 8 characters"
                  value={form.password}
                  onChange={handleChange}
                  autoComplete="new-password"
                />
                <Lock className="input-icon" />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label="Toggle password visibility"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="reg-confirm-password">
                Confirm Password
              </label>
              <div className="input-wrapper">
                <input
                  id="reg-confirm-password"
                  name="confirmPassword"
                  type={showPassword ? "text" : "password"}
                  className="form-input"
                  placeholder="Repeat your password"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  autoComplete="new-password"
                />
                <Lock className="input-icon" />
              </div>
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              id="register-submit"
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  Creating Account...
                </>
              ) : (
                "Create Account"
              )}
            </button>
          </form>

          <div className="auth-footer">
            Already have an account? <Link to="/login">Sign in</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
