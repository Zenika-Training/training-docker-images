import store from '../store/AuthenticationStore'
import axios from 'axios'

export default function auth({ next }) {
    axios.get("/api/v1/user/profile",{withCredentials: true})
    .then(
    response => {
        if(response.data.status=="error"){
            if(store.getters.isAuthenticated){
                store.commit('LOGOUT');
            }
        }
        else {
            if(!store.getters.isAuthenticated){
                store.commit('LOGIN',response.data.login);
            }
        }
    })
    return next();
}