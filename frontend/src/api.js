import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:7071/api";
const SHOW_HTTP_LOGS = process.env.REACT_APP_SHOW_HTTP_LOGS === "true";

const api = axios.create({ baseURL: API_BASE });

if (SHOW_HTTP_LOGS) {
	api.interceptors.request.use((config) => {
		console.log("➡️ Request:", config);
		return config;
	});
	api.interceptors.response.use(
		(response) => {
			console.log("⬅️ Response:", response);
			return response;
		},
		(error) => {
			console.error("❌ Error:", error);
			return Promise.reject(error);
		}
	);
}

export const login = (email, password) =>
	api.post("/user/login", { email, password });

export const register = (email, password, name) =>
	api.post("/user/register", { email, password, name });

export const getTasks = (token) =>
	api.get("/tasks", { headers: { Authorization: `Bearer ${token}` } });

export const createTask = (task, token) =>
	api.post("/tasks", task, { headers: { Authorization: `Bearer ${token}` } });

export const updateTask = (id, task, token) =>
	api.put(`/tasks/${id}`, task, {
		headers: { Authorization: `Bearer ${token}` },
	});

export const deleteTask = (id, token) =>
	api.delete(`/tasks/${id}`, { headers: { Authorization: `Bearer ${token}` } });

export const updateProfile = (user, token) =>
	api.put("/user/profile", user, {
		headers: { Authorization: `Bearer ${token}` },
	});

export const logout = () => localStorage.removeItem("token");
