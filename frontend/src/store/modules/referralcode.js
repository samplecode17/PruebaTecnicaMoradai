import apiClient from "@/services/appClient";

//configure a verification state on the global state
const state = {
  //will be necessary in future features
  //code: null,
  //codes: null,
  verification: null,
}

//is used to acces to the verification state of the global state of the page
const getters = {
  //will be necessary in future features
  //stateCode: state => state.code,
  //stateCodes: state => state.codes,
  stateVerification: state => state.verification,
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
  }
}

const mutations = {
  //set the response to the verification state of the global state
  setVerification(state, response) {
    state.verification = response;
  }
}


export default {
  state,
  getters,
  actions,
  mutations,
};
