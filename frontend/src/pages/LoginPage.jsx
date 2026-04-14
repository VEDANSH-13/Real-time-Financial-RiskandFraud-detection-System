import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Shield, User, Lock, Eye, EyeOff, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ username: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.username || !form.password) {
      setError("Please fill in all fields");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await login(form);
      navigate("/dashboard");
    } catch (err) {
      const msg =
        err.response?.data?.detail || "Login failed. Please try again.";
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
            <p>Real-Time Financial Risk Intelligence</p>
          </div>

          {/* Error alert */}
          {error && (
            <div className="alert alert-error">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          {/* Login form */}
          <form onSubmit={handleSubmit} id="login-form">
            <div className="form-group">
              <label className="form-label" htmlFor="login-username">
                Username
              </label>
              <div className="input-wrapper">
                <input
                  id="login-username"
                  name="username"
                  type="text"
                  className="form-input"
                  placeholder="Enter your username"
                  value={form.username}
                  onChange={handleChange}
                  autoComplete="username"
                />
                <User className="input-icon" />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="login-password">
                Password
              </label>
              <div className="input-wrapper">
                <input
                  id="login-password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  className="form-input"
                  placeholder="Enter your password"
                  value={form.password}
                  onChange={handleChange}
                  autoComplete="current-password"
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

            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              id="login-submit"
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  Authenticating...
                </>
              ) : (
                "Sign In"
              )}
            </button>
          </form>

          <div className="auth-footer">
            Don&apos;t have an account?{" "}
            <Link to="/register">Create one</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
