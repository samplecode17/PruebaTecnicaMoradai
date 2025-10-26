import apiClient from "@/services/appClient";

//token handling neede for the user enpoint call 
const token = localStorage.getItem("token");
if (token) {
  apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}


//configure a user state on the global state
const state = {
  user: null,
  usersById: {},
  userId: null,
  users:null,
};

//is used to acces to the user states of the global state of the page
const getters = {
  isAuthenticated: (state) => !!state.user,
  stateUser: (state) => state.user,
  getUserId: (state) => state.userId,
  getUserById: (state) => (id) => state.usersById[id] || null,
  getAllUsers: (state) => (state.users),
};

//enpoint calls
const actions = {
  async register({ dispatch }, form) {

    await apiClient.post("/users", form);
    const formData = new FormData();
    formData.append("username", form.username);
    formData.append("password", form.password);
    await dispatch("login", formData);
  },

  async login({ dispatch }, credentials) {
    try {
      const { data } = await apiClient.post("/auth/token", credentials);
      const token = data.token || data.access_token;

      localStorage.setItem("token", token);
      apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      await dispatch("Me");
    } catch (error) {
      localStorage.removeItem("token");
      delete apiClient.defaults.headers.common["Authorization"];
      throw error;
    }
  },

  async Me({ commit }) {
    try {
      const { data } = await apiClient.get("/auth/me");
      commit("setUser", data);
    } catch (error) {
      if (error.response?.status === 401) {
        commit("logout");
        localStorage.removeItem("token");
        delete apiClient.defaults.headers.common["Authorization"];
      }
    }
  },

  async getUser({ commit }, id) {
    try {
      const { data } = await apiClient.get(`/users/${id}`);
      commit("setUserById", data);
    } catch (error) {
      throw error;
    }
  },

  async getAllUsers({commit}){
    try{
      const {data} = await apiClient.get(`/users`)
      commit('setUsers',data)
    }catch (error) {
      throw error;
    }
  },

  async editUser({ dispatch }, { userId, form }) {
    try {
      const { data } = await apiClient.put(`/users/${userId}`, form);
      await dispatch("Me")
    } catch (error) {
      throw error;
    }
  },

  async deleteUser(_, id) {
    await apiClient.delete(`/users/${id}`);
  },

  async logOut({ commit }) {
    commit("logout");
    localStorage.removeItem("token");
    delete apiClient.defaults.headers.common["Authorization"];
  },
};

//set the responses of the actions to the user states on the global state
const mutations = {
  setUser(state, user) {
    state.user = user;
    state.userId = user.id;
  },
  setUsers(state,users){
    state.users = users;
  },
  setUserById(state, user) {
    state.usersById[user.id] = user;
  },
  logout(state) {
    state.user = null;
    state.userId = null;
    state.usersById = {};
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
