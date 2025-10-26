import apiClient from "@/services/appClient";

//configure a verification state on the global state
const state = {
  //will be necessary in future features
  //code: null,
  //codes: null,
  verification: null,
  creation: null,
}

//is used to acces to the verification state of the global state of the page
const getters = {
  //will be necessary in future features
  //stateCode: state => state.code,
  //stateCodes: state => state.codes,
  stateVerification: state => state.verification,
  stateCreation: state => state.creation,
}

//enpoint calls
const actions = {
  // calls the verification endpoint to 
  async verifyReferralCode({ commit }, code){
    try {
      const response = await apiClient.get(`/referalcodes/verify/${code}`);
      // extract the boolean
      const exists = response.data.exists;
      commit('setVerification', exists);
    } catch (err) {
      console.error('Error verifying code:', err);
      commit('setVerification', false); // por seguridad, ponemos false si falla
    }
  },

  async createReferralCode({ commit }, code) {
    try {
      const response = await apiClient.post(`/referalcodes`, code);
      if (response.data.response === "referralcode created") {
        commit('setCreation', true);
      } else {
        commit('setCreation', false);
      }
    } catch (err) {
      console.error('Error creating referral code:', err);
      commit('setCreation', false);
    }
  }
}

const mutations = {
  //set the response to the verification state of the global state
  setVerification(state, response) {
    state.verification = response;
  },
  setCreation(state, status) {
    state.creation = status;
  }
}


export default {
  state,
  getters,
  actions,
  mutations,
};
