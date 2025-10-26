import { createStore } from "vuex";
import users from "./modules/users";
import referralcode from "./modules/referralcode";


//handling the app global state creation  
export default createStore({
  modules: {
    users,
    referralcode,
  }
});