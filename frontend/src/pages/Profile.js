import { useState } from "react";
import { updateProfile, logout } from "../api";
import { useNavigate } from "react-router-dom";

function Profile() {
	const [form, setForm] = useState({ name: "", email: "" });
	const token = localStorage.getItem("token");
	const navigate = useNavigate();

	const handleUpdate = async (e) => {
		e.preventDefault();
		await updateProfile(form, token);
		alert("Perfil actualizado");
	};

	const handleLogout = () => {
		logout();
		navigate("/");
	};

	return (
		<div style={{ padding: "2rem" }}>
			<h2>Perfil</h2>
			<form onSubmit={handleUpdate}>
				<input
					placeholder='Nombre'
					value={form.name}
					onChange={(e) => setForm({ ...form, name: e.target.value })}
				/>
				<input
					placeholder='Email'
					value={form.email}
					onChange={(e) => setForm({ ...form, email: e.target.value })}
				/>
				<button type='submit'>Actualizar</button>
			</form>
			<button onClick={handleLogout}>Cerrar Sesión</button>
		</div>
	);
}

export default Profile;
