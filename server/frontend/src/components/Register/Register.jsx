import React, { useState } from "react";
import "./Register.css";
import userIcon from "../assets/person.png";
import emailIcon from "../assets/email.png";
import passwordIcon from "../assets/password.png";
import closeIcon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const register = async (event) => {
    event.preventDefault();

    const response = await fetch(`${window.location.origin}/djangoapp/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ userName, password, firstName, lastName, email }),
    });
    const data = await response.json();

    if (data.status === "Authenticated") {
      sessionStorage.setItem("username", data.userName);
      window.location.href = window.location.origin;
    } else if (data.error === "Already Registered") {
      alert("The user with the same username is already registered.");
    } else {
      alert(data.error || "The user could not be registered.");
    }
  };

  return (
    <div className="register_container">
      <div className="header register_header">
        <span className="text">Create an account</span>
        <a href="/" aria-label="Close registration">
          <img className="close_icon" src={closeIcon} alt="Close" />
        </a>
      </div>
      <form onSubmit={register}>
        <div className="inputs">
          <div className="input">
            <img src={userIcon} className="img_icon" alt="Username" />
            <input type="text" placeholder="Username" className="input_field" value={userName} onChange={(event) => setUserName(event.target.value)} required />
          </div>
          <div className="input">
            <img src={userIcon} className="img_icon" alt="First name" />
            <input type="text" placeholder="First name" className="input_field" value={firstName} onChange={(event) => setFirstName(event.target.value)} required />
          </div>
          <div className="input">
            <img src={userIcon} className="img_icon" alt="Last name" />
            <input type="text" placeholder="Last name" className="input_field" value={lastName} onChange={(event) => setLastName(event.target.value)} required />
          </div>
          <div className="input">
            <img src={emailIcon} className="img_icon" alt="Email" />
            <input type="email" placeholder="Email" className="input_field" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </div>
          <div className="input">
            <img src={passwordIcon} className="img_icon" alt="Password" />
            <input type="password" placeholder="Password" className="input_field" value={password} onChange={(event) => setPassword(event.target.value)} required />
          </div>
        </div>
        <div className="submit_panel">
          <input className="submit" type="submit" value="Register" />
        </div>
      </form>
    </div>
  );
};

export default Register;
